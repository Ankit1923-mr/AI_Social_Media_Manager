# routes/planner.py

from flask import Blueprint, request, jsonify
from app.services.scheduler import WeeklyScheduler

planner_bp = Blueprint("planner", __name__)
scheduler = WeeklyScheduler()

# 1. Generate schedule
@planner_bp.route("/", methods=["POST"])
def generate_schedule():
    try:
        data = request.json
        post_frequency = int(data.get("post_frequency"))
        preferred_days = data.get("preferred_days")

        if not isinstance(preferred_days, list):
            raise ValueError("Preferred days must be a list.")

        schedule = scheduler.generate_schedule(post_frequency, preferred_days)
        return jsonify(schedule), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 2. Get current schedule
@planner_bp.route("/", methods=["GET"])
def get_schedule():
    schedule = scheduler.get_schedule()
    if not schedule:
        return jsonify({"error": "No schedule has been generated yet."}), 404
    return jsonify(schedule), 200

# 3. Update post
@planner_bp.route("/<day>", methods=["PUT"])
def update_post(day):
    try:
        data = request.json
        new_content = data.get("content")

        updated_schedule = scheduler.update_post(day, new_content)
        return jsonify(updated_schedule), 200

    except KeyError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 4. Delete post
@planner_bp.route("/<day>", methods=["DELETE"])
def delete_post(day):
    try:
        updated_schedule = scheduler.delete_post(day)
        return jsonify(updated_schedule), 200

    except KeyError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 5. Reset entire schedule
@planner_bp.route("/reset", methods=["DELETE"])
def reset_schedule():
    scheduler.reset_schedule()
    return jsonify({"message": "Schedule reset successfully."}), 200
