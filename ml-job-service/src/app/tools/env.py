from collections import namedtuple


import os
from collections import namedtuple

ENV = {
    "CONTROLLER_HOST": os.getenv("CONTROLLER_HOST", "controller-service"),
    "CONTROLLER_PORT": os.getenv("CONTROLLER_PORT", "5000"),
    "CELERY_BROKER_URL": os.getenv("CELERY_BROKER_URL", "redis://redis:6379/1"),
    "CELERY_RESULT_BACKEND": os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1"),
    "MODEL_RMSE_THRESHOLD": float(os.getenv("MODEL_RMSE_THRESHOLD", "0.8")),
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
}

env = namedtuple("ENV", ENV.keys())(*ENV.values())
