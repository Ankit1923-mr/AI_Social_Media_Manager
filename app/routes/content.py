from flask import Blueprint, request, jsonify
from app.services.generator import generate_social_media_posts

content_bp = Blueprint("content", __name__)

@content_bp.route("/generate-posts", methods=["POST"])
def generate_posts():
    data = request.get_json()
    business_profile = {
        "name": data["name"],
        "industry": data["industry"]
    }
    preferences = {
        "tone": data["tone"],
        "post_type": data["post_type"]
    }
    news = data.get("news", [])
    count = int(data.get("count", 5))
    posts = generate_social_media_posts(business_profile, news, preferences, count)
    return jsonify({"posts": posts})

