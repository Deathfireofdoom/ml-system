from celery import shared_task
import requests

from app.utils.logger.logger import get_logger
logger = get_logger()

@shared_task(ignore_result=False)
def train_forecast_model():
    """
    Used for the weekly training of the forecast model
    """
    from datetime import datetime, timedelta
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
    end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = "/data/solar-dataset.pq"
    model_name = "forecast_model"

    body = {
        "file_path": file_path,
        "model_name": model_name,
        "start_date": start_date,
        "end_date": end_date,
    }

    # Call itself to invoke train job
    requests.post("http://controller:5000/job/train", json=body)

    # Log the start of the training job
    logger.info(f"Started scheduled training job for {model_name} with {body}")

    return "Started training job"


@shared_task(ignore_result=False)
def predict_forecast_model():
    """
    Used for the daily prediction of the forecast model
    """
    from datetime import datetime, timedelta

    start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    file_path = "/data/solar-dataset.pq"
    model_name = "forecast_model"

    body = {
        "file_path": file_path,
        "model_name": model_name,
        "start_date": start_date,
        "end_date": end_date,
    }

    # Call itself to invoke predict job
    requests.post("http://controller:5000/job/predict", json=body)

    # Log the start of the predict job
    logger.info(f"Started scheduled prediction job for {model_name} with {body}")

    return "prediction job started"
