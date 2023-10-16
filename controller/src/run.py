from app import create_app

# Hacky slution to make celery discover tasks - There is probably a better way to do this
from app.tasks.job import train_forecast_model, predict_forecast_model


flask_app = create_app()
flask_app.debug = True
celery_app = flask_app.extensions["celery"]

if __name__ == "__main__":
    flask_app.run(host="localhost", port=5000, debug=True)
