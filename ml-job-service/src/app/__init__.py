from flask import Flask
from app.celery_config import celery_init_app
import os

# routes
from app.routes.health import health
from app.routes.train import train
from app.routes.predict import predict


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://redis:6379/0",
            result_backend="redis://redis:6379/0",
            task_ignore_result=True,
        ),
    )
    # If you use from_prefixed_env(), ensure that your environment variables are set properly
    app.config.from_prefixed_env()
    celery_init_app(app)

    # register routes
    app.register_blueprint(health, url_prefix="/health")
    app.register_blueprint(train, url_prefix="/train")
    app.register_blueprint(predict, url_prefix="/predict")

    return app
