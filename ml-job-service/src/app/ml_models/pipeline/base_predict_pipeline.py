import random
import string
from datetime import datetime
import pandas as pd

from app.tools.logger import get_logger
logger = get_logger()


class PredictPipeline:
    def __init__(
        self,
        model_name,
        model_source,
        data_source,
        data_sink,
        data_transformer,
        model_registry,
    ):
        self.model_name = model_name
        self.model_source = model_source
        self.data_source = data_source
        self.data_sink = data_sink
        self.data_transformer = data_transformer
        self.model_registry = model_registry

    def run(self):
        # start run
        start_time = datetime.now()
        run_id = self._get_run_identifier()
        logger.info(f"Starting run {run_id} for model {self.model_name}")


        # get model
        logger.info(f"Getting model for run {run_id}")
        try:
            model = self.model_source.load_model()
        except Exception as e:
            logger.error(f"Failed to load model for run {run_id}")
            raise e

        # get dataframe from data source
        logger.info(f"Getting dataframe from data source for run {run_id}")
        try:
            df = self.data_source.get_dataframe()
        except Exception as e:
            logger.error(f"Failed to get dataframe from data source for run {run_id}")
            raise e

        # transform dataframe
        logger.info(f"Transforming dataframe for run {run_id}")
        try:
            index, X = self.data_transformer.transform(df)
        except Exception as e:
            logger.error(f"Failed to transform dataframe for run {run_id}")
            raise e

        # predict
        logger.info(f"Predicting for run {run_id}")
        try:
            y_pred = model.predict(X)
        except Exception as e:
            logger.error(f"Failed to predict for run {run_id}")
            raise e

        # create prediction dataframe
        logger.info(f"Creating prediction dataframe for run {run_id}")
        try:
            df = self._create_prediction_dataframe(index, y_pred)
        except Exception as e:
            logger.error(f"Failed to create prediction dataframe for run {run_id}")
            raise e

        # save predictions
        logger.info(f"Saving predictions for run {run_id}")
        try:
            self.data_sink.save_dataframe(df, self.model_name, run_id)
        except Exception as e:
            logger.error(f"Failed to save predictions for run {run_id}")
            raise e

        # register run
        run_duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        run_metadata = self._get_run_metadata(
            run_id=run_id,
            run_start_time=start_time,
            run_duration_ms=run_duration_ms,
            model_version_id=self.model_source.get_model_version_identifier(),
            run_metadata=self.model_source.get_model_metadata(),
        )
        logger.info(f"Registering run for run {run_id} with metadata {run_metadata}")
        try:
            self.model_registry.register_run(run_metadata)
        except Exception as e:
            logger.error(f"Failed to register run for run {run_id}")
            raise e

    @staticmethod
    def _create_prediction_dataframe(index, y_pred):
        return pd.DataFrame(data=y_pred, index=index, columns=["prediction"])

    def _get_run_metadata(
        self, run_id, run_start_time, run_duration_ms, model_version_id, run_metadata
    ):
        run_metadata = {
            "run_id": run_id,
            "run_start_time": run_start_time.isoformat(),
            "run_duration_ms": run_duration_ms,
            "run_type": "prediction",
            "model_name": self.model_name,
            "model_version_id": model_version_id,
            "run_metadata": run_metadata,
        }
        return run_metadata

    @staticmethod
    def _get_run_identifier(length: int = 10):
        letters = string.ascii_letters
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str
