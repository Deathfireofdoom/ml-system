from flask import Blueprint, jsonify
from datetime import datetime

health = Blueprint("health", __name__)


@health.route("/", methods=["GET"])
def health_route():
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"message": f"everything is fine att {date_str}"}), 200
