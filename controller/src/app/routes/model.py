from flask import Blueprint, jsonify
from flask import request
from app.utils.logger.logger import get_logger
from app.services.model_registry_service import (
    new_model_registry_service_with_redis_pub_sub,
)

logger = get_logger()

model = Blueprint("model", __name__)


@model.route("/register", methods=["POST"])
def register_model_route():
    # get request body
    body = request.get_json()

    # validate request body
    if not body:
        return jsonify({"message": "request body is required"}), 400

    # validate request body
    if not body.get("model_name"):
        return jsonify({"message": "model_name is required"}), 400

    # validate request body
    if not body.get("model_version_id"):
        return jsonify({"message": "model_version_id is required"}), 400

    # logging request
    logger.info(f"Got model register request with body: {body}")

    # create body
    model_name = body.pop("model_name")
    model_version_id = body.pop("model_version_id")

    # get model registry service
    model_registry_service = new_model_registry_service_with_redis_pub_sub()
    model_registry_service.add_run(
        model_name=model_name, model_version_id=model_version_id, model_metadata=body
    )

    return jsonify({"message": "model registered"}), 200

@model.route("/promote", methods=["POST"])
def promote_model_route():
    # get request body
    body = request.get_json()

    # validate request body
    if not body:
        return jsonify({"message": "request body is required"}), 400
    
    # validate request body
    if not body.get("model_name"):
        return jsonify({"message": "model_name is required"}), 400
    
    # validate request body
    if not body.get("model_version_id"):
        return jsonify({"message": "model_version_id is required"}), 400
    
    # logging request
    logger.info(f"Got model promote request with body: {body}")

    # create body
    model_name = body.pop("model_name")
    model_version_id = body.pop("model_version_id")

    # get model registry service
    model_registry_service = new_model_registry_service_with_redis_pub_sub()
    model_registry_service.promote_model(
        model_name=model_name, model_version_id=model_version_id
    )

    return jsonify({"message": "model promoted"}), 200

@model.route("/demote", methods=["GET"])
def demote_model_route():
    # get model name from query string
    model_name = request.args.get("model_name")

    # validate model name
    if not model_name:
        return jsonify({"message": "model_name is required"}), 400
    
    # logging request
    logger.info(f"Got model demote request with model_name: {model_name}")

    # get model registry service
    model_registry_service = new_model_registry_service_with_redis_pub_sub()

    # demote model
    model_registry_service.demote_model(model_name=model_name)

    return jsonify({"message": "model demoted"}), 200



