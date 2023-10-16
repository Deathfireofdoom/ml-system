from collections import namedtuple


import os
from collections import namedtuple

ENV = {
    "DB_HOST": os.getenv("DB_HOST", "postgres"),
    "DB_PORT": os.getenv("DB_PORT", "5432"),
    "DB_NAME": os.getenv("DB_NAME", "postgres"),
    "DB_USER": os.getenv("DB_USER", "postgres"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
    "CELERY_BROKER_URL": os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    "CELERY_RESULT_BACKEND": os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    "REDIS_HOST": os.getenv("REDIS_HOST", "redis"),
    "REDIS_PORT": os.getenv("REDIS_PORT", "6379"),
    "ML_JOB_SERVICE_HOST": os.getenv("ML_JOB_SERVICE_URL", "ml-job-service"),
    "ML_JOB_SERVICE_PORT": os.getenv("ML_JOB_SERVICE_PORT", "5050"),
}

env = namedtuple("ENV", ENV.keys())(*ENV.values())
