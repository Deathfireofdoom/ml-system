from flask import Blueprint, jsonify
from app.tasks.health import health_check

health = Blueprint("health", __name__)


@health.route("/", methods=["GET"])
def health_route():
    return jsonify({"message": "everything is fine"}), 200


@health.route("/celery", methods=["GET"])
def health_celery_route():
    result = health_check.delay()
    return jsonify({"message": result.get()}), 200
