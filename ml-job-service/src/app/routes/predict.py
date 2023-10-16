from flask import Blueprint, jsonify, request
from datetime import datetime

from app.tasks.forecast_model import run_predict
from app.tools.logger import get_logger

logger = get_logger()

predict = Blueprint("predict", __name__)


@predict.route("/forecast_model", methods=["POST"])
def predict_forecast_route():
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
        "model_metadata": {
            "model_destination": {
                "location_type": "localfile",
                "file_path": "/model/forecast_model/GakcjKXcZR.joblib",
                "model_version_identifier": "GakcjKXcZR",
                "load_type": "joblib",
            },
        },
    }

    # get request body
    body = request.get_json()

    # merge defaults with body
    params = {**defaults, **body}
    
    # Call the task to run the prediction in celery worker
    run_predict.delay(**params)

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"message": f"Model has been predicting at {date_str}"}), 200
