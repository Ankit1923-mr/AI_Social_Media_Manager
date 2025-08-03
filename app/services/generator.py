import os
import re
import requests

# Load GROQ API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY must be set in your environment.")

# GROQ API endpoint and model
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"


def generate_social_media_posts(business_profile, news, preferences, count=5):
    """
    Generates a list of ready-to-publish social media post captions.

    Args:
        business_profile (dict): Should include keys like 'name', 'industry', etc.
        news (list): List of trending news headlines or topics (strings).
        preferences (dict): Dict with 'tone' (str), 'post_type' (str).
        count (int): Number of posts to generate.

    Returns:
        list of post strings.
    """

    name = business_profile.get("name", "Your Business")
    industry = business_profile.get("industry", "your industry")
    tone = preferences.get("tone", "informative").lower()
    post_type = preferences.get("post_type", "general").lower()

    if post_type == "promo":
        prompt_intro = f"Generate {count} unique social media posts with a {tone} tone for a promotional campaign for a {industry} business named {name}."
    elif post_type in ["business_tips", "tip"]:
        prompt_intro = f"Generate {count} unique social media posts with a {tone} tone sharing business tips for a {industry} business named {name}."
    elif post_type in ["industry_insights", "update"]:
        prompt_intro = f"Generate {count} unique social media posts with a {tone} tone offering insights about the {industry} industry for a business named {name}."
    elif post_type == "seasonal":
        prompt_intro = f"Generate {count} unique social media posts with a {tone} tone for seasonal greetings or announcements for a {industry} business named {name}."
    else:
        prompt_intro = f"Generate {count} unique social media posts with a {tone} tone with general content for a {industry} business named {name}."

    # Add trending topics if available
    if news:
        prompt_intro += " Also consider the following trending topics: " + ", ".join(news) + "."

    # Formatting requirements
    prompt_intro += (
        " Include relevant hashtags. "
        "Avoid emojis, markdown symbols like **, and any unicode escape characters. "
        "Return plain text only. Number each post or separate posts by newlines."
    )

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You're a helpful assistant that writes catchy social media content."},
            {"role": "user", "content": prompt_intro}
        ],
        "temperature": 0.6,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(GROQ_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    raw_output = response.json()["choices"][0]["message"]["content"]

    # Clean and split generated posts
    split_posts = re.split(r'\n\d+\.\s*|\n-\s*|\n•\s*|\n', raw_output)
    cleaned_posts = []
    for post in split_posts:
        clean = post.strip()
        clean = re.sub(r"\*+", "", clean)
        clean = re.sub(r"\\u[\da-fA-F]{4}", "", clean)
        clean = re.sub(r"[^\x20-\x7E#]", "", clean)
        if clean:
            cleaned_posts.append(clean)

    return cleaned_posts[:count]
