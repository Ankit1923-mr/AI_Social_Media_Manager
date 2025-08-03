import feedparser

def fetch_industry_name(business_profile: dict) -> str:
    """
    Extract industry name from a business profile dictionary.

    Args:
        business_profile (dict): Parsed business profile JSON.

    Returns:
        str: Industry name or empty string if not found.
    """
    # Safe extraction with fallback to empty string
    return business_profile.get("industry", "").strip()

def fetch_industry_news(industry: str):
    """
    Fetch the latest top 5 news headlines related to the given industry
    from Google News RSS feed.

    Args:
        industry (str): Industry name to search news for.

    Returns:
        List[dict]: List of news items as dicts with 'headline' and 'url'.
    """
    if not industry:
        return []

    # Prepare search query by replacing spaces with '+'
    query = industry.replace(" ", "+")
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)

    headlines = []
    for entry in feed.entries[:5]:
        headlines.append({
            "headline": entry.title,
            "url": entry.link if 'link' in entry else None
        })
    return headlines

def fetch_news_from_business_profile(business_profile: dict):
    """
    Convenience function: Takes the business profile dict,
    extracts the industry, and fetches the top 5 news for it.

    Args:
        business_profile (dict): Business profile as parsed from LLM.

    Returns:
        List[dict]: List of news items (headline + url).
    """
    industry = fetch_industry_name(business_profile)
    return fetch_industry_news(industry)
