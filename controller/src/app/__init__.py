from flask import Flask
from app.celery_config import celery_init_app
from app.utils.env.env import env

# routes
from app.routes.health import health
from app.routes.migrate import migrate
from app.routes.model import model
from app.routes.run import run
from app.routes.job import job


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=env.CELERY_BROKER_URL,
            result_backend=env.CELERY_RESULT_BACKEND,
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)

    # register routes
    app.register_blueprint(health, url_prefix="/health")
    app.register_blueprint(migrate, url_prefix="/migrate")
    app.register_blueprint(model, url_prefix="/model")
    app.register_blueprint(run, url_prefix="/run")
    app.register_blueprint(job, url_prefix="/job")

    return app
