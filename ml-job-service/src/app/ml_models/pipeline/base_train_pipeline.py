from datetime import datetime
import string
import random

from app.tools.logger import get_logger
logger = get_logger()


class TrainingPipeline:
    def __init__(
        self,
        model_name: str,
        data_source,
        data_transformer,
        model_destination,
        model_generator,
        model_validator,
        model_registry,
    ):
        self.model_name = model_name
        self.data_source = data_source
        self.data_transformer = data_transformer
        self.model_destination = model_destination
        self.model_generator = model_generator
        self.model_validator = model_validator
        self.model_registry = model_registry

    def run(self, model_version_id: str = None):
        """
        Runs each step in the training pipeline.
        """
        # start run
        start_time = datetime.now()
        run_id = self._get_run_identifier()
        if not model_version_id:
            model_version_id = self._get_model_identifier()

        # log run
        logger.info(f"Starting run {run_id} for model {self.model_name}")

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
            X_train, X_test, y_train, y_test = self.data_transformer.transform(df)
        except Exception as e:
            logger.error(f"Failed to transform dataframe for run {run_id}")
            raise e

        # train model
        logger.info(f"Training model for run {run_id}")
        try:
            model, model_run_metadata = self.model_generator.train(X_train, y_train)
        except Exception as e:
            logger.error(f"Failed to train model for run {run_id}")
            raise e
        logger.info(f"Trained model for run {run_id} with metadata {model_run_metadata}")

        # validate model
        logger.info(f"Validating model for run {run_id}")
        try:
            validation_results = self.model_validator.validate(model, X_test, y_test)
        except Exception as e:
            logger.error(f"Failed to validate model for run {run_id}")
            raise e

        # save model
        logger.info(f"Saving model for run {run_id}")
        try:
            model_destination = self.model_destination.save_model(
                model, self.model_name, model_version_id
            )
        except Exception as e:
            logger.error(f"Failed to save model for run {run_id}")
            raise e

        # register model
        model_metadata = self._get_model_metadata(
            run_id=run_id,
            model_version_id=model_version_id,
            model_run_metadata=model_run_metadata,
            validation_results=validation_results,
            model_destination=model_destination,
        )
        logger.info(f"Registering model for run {run_id} with metadata {model_metadata}")
        try:
            self.model_registry.register_model(model_metadata)
        except Exception as e:
            logger.error(f"Failed to register model for run {run_id}")
            raise e

        # register run
        run_duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        run_metadata = self._get_run_metadata(
            run_id=run_id,
            run_start_time=start_time,
            run_duration_ms=run_duration_ms,
            model_version_id=model_version_id,
            model_run_metadata=model_run_metadata,
        )
        logger.info(f"Registering run for run {run_id} with metadata {run_metadata}")
        try:
            self.model_registry.register_run(run_metadata)
        except Exception as e:
            logger.error(f"Failed to register run for run {run_id}")
            raise e

        # log run
        logger.info(f"Finished run {run_id} for model {self.model_name} took {run_duration_ms} ms")

    def _get_model_metadata(
        self,
        run_id,
        model_version_id,
        model_run_metadata,
        validation_results,
        model_destination,
    ):
        model_metadata = {
            "model_name": self.model_name,
            "model_version_id": model_version_id,
            "model_destination": model_destination,
            "model_metrics": validation_results,
            "model_run_metadata": model_run_metadata,
            "run_id": run_id,
        }
        return model_metadata

    def _get_run_metadata(
        self,
        run_id,
        run_start_time,
        run_duration_ms,
        model_version_id,
        model_run_metadata,
    ):
        run_metadata = {
            "run_id": run_id,
            "run_start_time": run_start_time.isoformat(),
            "run_duration_ms": run_duration_ms,
            "run_type": "training",
            "model_name": self.model_name,
            "model_version_id": model_version_id,
            "run_metadata": model_run_metadata,
        }
        return run_metadata

    @staticmethod
    def _get_model_identifier(length: int = 10):
        letters = string.ascii_letters
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str

    @staticmethod
    def _get_run_identifier(length: int = 10):
        letters = string.ascii_letters
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str
