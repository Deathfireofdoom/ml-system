from app import create_app

# - Hacky solution to make celery find the tasks
from app.tasks.forecast_model import run_predict, run_train

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

if __name__ == "__main__":
    flask_app.run(host="localhost", port=5000, debug=True)
