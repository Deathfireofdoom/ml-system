from celery import shared_task
from app.ml_models.forecast_model import ForecastModel

@shared_task(ignore_result=False)
def run_predict(**params):
    forecast_model = ForecastModel()
    forecast_model.predict(**params)

@shared_task(ignore_result=False)
def run_train(**params):
    forecast_model = ForecastModel()
    forecast_model.train(**params)
