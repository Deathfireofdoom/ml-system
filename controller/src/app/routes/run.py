from flask import Blueprint, jsonify
from flask import request
from app.utils.logger.logger import get_logger
from app.services.run_registry_service import (
    new_run_registry_service_with_redis_pub_sub,
)

logger = get_logger()

run = Blueprint("run", __name__)


@run.route("/register", methods=["POST"])
def register_run_route():
    # get request body
    body = request.get_json()

    # validate request body
    if not body:
        return jsonify({"message": "request body is required"}), 400

    # validate request body
    if not body.get("run_id"):
        return jsonify({"message": "run_id is required"}), 400

    # validate request body
    if not body.get("run_start_time"):
        return jsonify({"message": "run_start_time is required"}), 400

    # validate request body
    if not body.get("run_duration_ms"):
        return jsonify({"message": "run_duration_ms is required"}), 400

    # validate request body
    if not body.get("run_type"):
        return jsonify({"message": "run_type is required"}), 400

    # validate request body
    if not body.get("model_name"):
        return jsonify({"message": "model_name is required"}), 400

    # validate request body
    if not body.get("model_version_id"):
        return jsonify({"message": "model_version_id is required"}), 400

    # validate request body
    if not body.get("run_metadata"):
        return jsonify({"message": "run_metadata is required"}), 400

    # logging request
    logger.info(f"Got run register request with body: {body}")

    # get run registry service
    run_registry_service = new_run_registry_service_with_redis_pub_sub()
    run_registry_service.add_run(
        run_id=body.get("run_id"),
        run_start_time=body.get("run_start_time"),
        run_duration_ms=body.get("run_duration_ms"),
        run_type=body.get("run_type"),
        model_name=body.get("model_name"),
        model_version_id=body.get("model_version_id"),
        run_metadata=body.get("run_metadata"),
    )

    return jsonify({"message": "run registered"}), 200
