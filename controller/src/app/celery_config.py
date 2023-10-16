from celery import Celery, Task
from celery.schedules import crontab


def celery_init_app(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()

    # Setup periodic tasks
    celery_app.conf.beat_schedule = {
        "health-task": {
            "task": "app.tasks.health.health_cron_check",
            "schedule": crontab(minute="*/10"),
        },
        "train-forecast-model": {
            "task": "app.tasks.job.train_forecast_model",
            "schedule": crontab(
                day_of_week=1, hour=12, minute=0
            ),  # NOTE: This is a arbitrary time, but it is scheduled to run once a week.
                #       In real life this would be set with regards to the data availability etc.
        },
        "predict-forecast-model": {
            "task": "app.tasks.job.predict_forecast_model",
            "schedule": crontab(
                hour=11, minute=50
            ), # NOTE: This is a arbitrary time with following considerations:
               # 1. Give some time for the prediction to run.
               # 2. Give some time for a re-try to run if the prediction fails. THIS IS NOT IMPLEMENTED
               #
               # NOTE: Instead of cron job I would more likely make some kind of pub/sub system where the
               #      prediction is triggered by a message from the ETL pipeline when new data is available.
        },
    }

    app.extensions["celery"] = celery_app
    return celery_app
