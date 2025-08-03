import os
import json
import requests

FB_CREDENTIALS_FILE = "fb_credentials.json"

def connect_facebook_page():
    """
    Simulate a 1-click Facebook page connection.
    Returns a mock page ID and access token.
    """
    return {
        "status": "connected",
        "fb_page_id": "1234567890",
        "access_token": "mock_fb_access_token"
    }

def save_fb_credentials(creds):
    """
    Save Facebook credentials to a local JSON file.
    """
    with open(FB_CREDENTIALS_FILE, "w") as f:
        json.dump(creds, f)

def load_fb_credentials():
    """
    Load Facebook credentials from the local JSON file.
    Returns an empty dict if not found.
    """
    if os.path.exists(FB_CREDENTIALS_FILE):
        with open(FB_CREDENTIALS_FILE, "r") as f:
            return json.load(f)
    return {}

def publish_to_facebook(post_message: str, fb_page_id: str, access_token: str):
    """
    Publish a message to the Facebook Page (mocked).
    Returns a structure with post_id and post_link.
    """
    post_id = f"mock_post_{abs(hash(post_message)) % 1_000_000}"
    post_link = f"https://facebook.com/{fb_page_id}/posts/{post_id}"
    return {
        "success": True,
        "post_id": post_id,
        "post_link": post_link
    }

    # ---- Uncomment for actual Facebook API integration ----
    # url = f"https://graph.facebook.com/{fb_page_id}/feed"
    # payload = {"message": post_message, "access_token": access_token}
    # resp = requests.post(url, data=payload)
    # resp.raise_for_status()
    # data = resp.json()
    # return {"success": True, "post_id": data["id"], "post_link": data["id"]}
