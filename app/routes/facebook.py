from flask import Blueprint, request, jsonify
from app.services.facebook import (
    connect_facebook_page, publish_to_facebook,
    save_fb_credentials, load_fb_credentials
)
from app.services.scheduler import WeeklyScheduler

facebook_bp = Blueprint("facebook", __name__)

@facebook_bp.route("/connect", methods=["GET", "POST"])
def fb_connect():
    """
    GET/POST /api/facebook/connect
    Simulate Facebook connection and persist credentials to JSON file.
    """
    creds = connect_facebook_page()
    save_fb_credentials({
        "fb_page_id": creds["fb_page_id"],
        "access_token": creds["access_token"]
    })
    return jsonify(creds), 200

@facebook_bp.route("/publish", methods=["GET", "POST"])
def fb_publish():
    """
    GET  /api/facebook/publish?day=Mon[&message=...]
    POST /api/facebook/publish { "day": "...", "message": "..." }
    Publishes the scheduled (or override) message for the given weekday.
    """
    if request.method == "GET":
        day = request.args.get("day")
        override_msg = request.args.get("message")
    else:
        data = request.get_json() or {}
        day = data.get("day")
        override_msg = data.get("message")

    creds = load_fb_credentials()
    page_id = creds.get("fb_page_id")
    token = creds.get("access_token")
    if not page_id or not token:
        return jsonify({"error": "Facebook page not connected"}), 400

    scheduler = WeeklyScheduler()
    schedule = scheduler.get_schedule()
    if not day:
        return jsonify({"error": "Missing 'day' parameter"}), 400
    if day not in schedule:
        return jsonify({"error": f"No scheduled post for '{day}'"}), 404

    message = override_msg or schedule[day]
    result = publish_to_facebook(message, page_id, token)
    print(result)
    return jsonify(result), 200
