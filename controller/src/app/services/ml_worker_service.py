import requests

from app.utils.env.env import env
from app.utils.logger.logger import get_logger

logger = get_logger()

class MlJobService:
    def __init__(self, host: str = None, port: str = None) -> None:
        if not host:
            host = env.ML_JOB_SERVICE_HOST
        if not port:
            port = env.ML_JOB_SERVICE_PORT
        
        self.url = f"http://{host}:{port}"

    def submit_training_job(self, job_metadata: dict):
        # Get model name from job metadata
        model_name = job_metadata["model_name"]

        # Build url
        url = f"{self.url}/train/{model_name}"

        # logging
        logger.info(f"Submitting training job to {url} with {job_metadata}")

        # Send request
        requests.post(url=url, json=job_metadata)
        

    def submit_prediction_job(self, job_metadata: dict):
        # Get model name from job metadata
        model_name = job_metadata["model_name"]

        # Build url
        url = f"{self.url}/predict/{model_name}"

        # Check if model version is specified - if not, use latest
        if not job_metadata.get("model_version_id"):
            # get latest model version id from repository
            from app.repository.model_log_repository import ModelLogRepostiory
            model_tuple = ModelLogRepostiory().get_current_model(model_name)
            if not model_tuple:
                raise Exception(f"Model {model_name} not found")
            
            job_metadata["model_version_id"] = model_tuple[1]
            job_metadata["model_metadata"] = model_tuple[2]

        # logging
        logger.info(f"Submitting training job to {url} with {job_metadata}")

        # Send request
        requests.post(url=url, json=job_metadata)
