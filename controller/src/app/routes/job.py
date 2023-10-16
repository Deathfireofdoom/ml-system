from flask import Blueprint, jsonify, request

from app.services.ml_worker_service import MlJobService
from app.utils.logger.logger import get_logger

logger = get_logger()


job = Blueprint("job", __name__)


@job.route("/train", methods=["POST"])
def train_route():
    # Get job parameters from request body
    body = request.get_json()
    
    # logging
    logger.info(f"Got train request with body: {body}")

    # Call ml-job-service
    MlJobService().submit_training_job(body)

    return jsonify({"message": "Train job has started"}), 200


@job.route("/predict", methods=["POST"])
def predict_route():
    # Get job parameters from request body
    body = request.get_json()

    # logging
    logger.info(f"Got predict request with body: {body}")

    # Call ml-job-service
    MlJobService().submit_prediction_job(body)
    return jsonify({"message": "Predict job has started."}), 200
