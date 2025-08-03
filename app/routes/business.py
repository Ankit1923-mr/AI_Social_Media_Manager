from flask import Blueprint, request, jsonify
from app.services.scraper import fetch_html, extract_visible_content, fetch_html_title, analyze_website_business_profile


business_bp = Blueprint("business", __name__)


@business_bp.route("/profile", methods=["POST"])
def generate_business_profile():
    data = request.get_json()
    url = data.get("website_url")

    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        html = fetch_html(url)
        text_content = extract_visible_content(html)
        title = fetch_html_title(html)
        profile = analyze_website_business_profile(text_content, title=title)
        return jsonify({"profile": profile}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
