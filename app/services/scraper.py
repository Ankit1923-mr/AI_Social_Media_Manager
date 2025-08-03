import os
import re
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from groq import Groq  # Groq SDK

# Load environment variables (adjust .env path as needed)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

# Load Groq API key from env variable GROQ_API_KEY
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Initialize Groq client with your API key
client = Groq(api_key=groq_api_key)


def fetch_html(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL {url} — Status code: {response.status_code}")
    return response.text


def extract_visible_content(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "meta", "noscript", "iframe"]):
        tag.decompose()
    tags = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "li"])
    text_chunks = [tag.get_text(strip=True) for tag in tags if tag.get_text(strip=True)]
    extracted_text = "\n".join(text_chunks)
    print("==== Extracted Visible Content (first 2000 chars) ====")
    print(extracted_text[:2000])
    print("==== End of Extracted Content ====")
    return extracted_text


def fetch_html_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return ""


def clean_json_response(response_text: str) -> dict:
    """
    Clean and parse JSON from LLM output by removing markdown code fences.

    Args:
        response_text (str): Raw response content from LLM including markdown code fences.

    Returns:
        dict: Parsed JSON object.

    Raises:
        json.JSONDecodeError: If JSON parsing fails.
    """
    # Remove possible opening `````` and trailing ```
    cleaned = re.sub(r"^```(?:json)?\s*", "", response_text)  # Remove leading ```
    cleaned = re.sub(r"\s*```$", "", cleaned)  # Remove trailing ```
    cleaned = cleaned.strip()
    return json.loads(cleaned)


def analyze_website_business_profile(content: str, title: str = "") -> dict:
    """
    Use Groq llama-3.1-8b-instant model to analyze website content.
    Pass the page title explicitly to help business name detection.
    """

    prompt_content = content
    if title:
        prompt_content = f"Website Title: {title}\n\n{content}"

    messages = [
        {
            "role": "system",
            "content": (
                "You are a business analyst AI agent. "
                "Given the text extracted from a company's website, infer the following fields: "
                "name, industry, services, audience, tone_of_voice, unique_value_proposition. "
                "Return only a JSON object with these keys and no additional explanation."
            )
        },
        {
            "role": "user",
            "content": prompt_content[:10000]  # Limit content length per request
        }
    ]

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
    )

    result_text = completion.choices[0].message.content
    print("==== Raw Model Output ====")
    print(result_text)
    print("==== End Raw Output ====")

    # Parse JSON from the model response
    try:
        profile = clean_json_response(result_text)
    except Exception as e:
        print("==== ERROR: Failed JSON parsing ====")
        print(result_text)
        raise ValueError(f"JSON parse error: {e}")

    return profile


def main():
    url = input("Enter website URL (e.g. https://www.dominos.co.in): ").strip()

    try:
        print("🌐 Fetching website content...")
        html = fetch_html(url)

        print("🔍 Extracting visible text from HTML...")
        text_content = extract_visible_content(html)

        print("🔍 Extracting page title from HTML...")
        title = fetch_html_title(html)

        print("\n📝 Content preview (first 500 chars):\n")
        print(text_content[:500] + "...\n")

        print("🤖 Analyzing business profile via Groq llama-3.1-8b-instant model...\n")
        profile = analyze_website_business_profile(text_content, title=title)

        print("✅ Business Profile Extracted:\n")
        print(json.dumps(profile, indent=2))

    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
