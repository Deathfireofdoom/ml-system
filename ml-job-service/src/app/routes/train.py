from flask import Blueprint, jsonify, request
from datetime import datetime
from app.tools.logger import get_logger

from app.tasks.forecast_model import run_train

logger = get_logger()

train = Blueprint("train", __name__)


@train.route("/forecast_model", methods=["POST"])
def train_forecast_model_route():
    # get the parameters from the body
    # DISCLAIMER:
    # Since this is just a test case I opted to add some default values like start_date, end_date and model_metadata.
    # In production this would not make sense, instead we would throw an error if the user did not provide
    # start_date, end_date and model_metadata.
    #
    # if not body.get("start_date"):
    #     return jsonify({"message": "Missing start_date"}), 400
    # if not body.get("end_date"):
    #     return jsonify({"message": "Missing end_date"}), 400
    # if not body.get("model_metadata"):
    #     return jsonify({"message": "Missing model_metadata"}), 400
    #
    # But for now we will just add some default values to make it easier to invoke the endpoint.

    defaults = {
        "file_path": "/data/solar-dataset.pq",
        "start_date": "2017-01-01",
        "end_date": "2017-01-02",
    }

    # get request body
    body = request.get_json()

    # merge defaults with body
    params = {**defaults, **body}

    # Call the task to run the training in celery worker
    run_train.delay(**params)
    
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"message": f"Model has been trained at {date_str}"}), 200
