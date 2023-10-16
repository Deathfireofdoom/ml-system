from app.ml_models.pipeline.base_train_pipeline import TrainingPipeline
from app.ml_models.pipeline.base_predict_pipeline import PredictPipeline
from app.ml_models.pipeline.components.data_source.data_source import (
    LocalParquetDataSource,
)
from app.ml_models.pipeline.components.data_transformer.data_transformer import (
    ForecastTrainDataTransformer,
    ForecastPredictDataTransformer,
)
from app.ml_models.pipeline.components.model_generator.model_generator import (
    ForecastModelGenerator,
)
from app.ml_models.pipeline.components.model_validator.model_validator import (
    ForecastModelValidator,
)
from app.ml_models.pipeline.components.model_destination.model_destination import (
    LocalFileModelDestination,
)
from app.ml_models.pipeline.components.model_source.model_source import (
    LocalFileModelSource,
)
from app.ml_models.pipeline.components.data_sink.data_sink import LocalCsvDataSink

from app.ml_models.pipeline.components.model_registry.model_registry import (
    new_controller_model_registry_basic_client,
)


class ForecastModel:
    def train(
        self,
        file_path: str,
        start_date: str,
        end_date: str,
        interval_date_column: str = "start_of_quarter",
        time_travel: bool = False,
        time_travel_date: str = None,
        time_travel_date_column: str = "created_at",
        test_size: float = 0.2,
        n_estimators: int = 500,
        min_impurity_decrease: float = 1e-4,
        min_samples_leaf: int = 30,
        max_samples: float = 0.7,
        n_jobs: int = 4,
        **kwargs, # Make it easier to add new parameters later but also bad.
    ):
        # Setting up the datasource
        data_source = LocalParquetDataSource(
            file_path=file_path,
            start_date=start_date,
            end_date=end_date,
            interval_date_column=interval_date_column,
            time_travel=time_travel,
            time_travel_date=time_travel_date,
            time_travel_date_column=time_travel_date_column,
        )

        # Setting up the transformer
        data_transformer = ForecastTrainDataTransformer(test_size=test_size)

        # Setting up the model generator
        model_generator = ForecastModelGenerator(
            n_estimators=n_estimators,
            min_impurity_decrease=min_impurity_decrease,
            min_samples_leaf=min_samples_leaf,
            max_samples=max_samples,
            n_jobs=n_jobs,
        )

        # Setting up the model validator
        model_validator = ForecastModelValidator()

        # Setting up model destination
        model_destination = LocalFileModelDestination(base_file_path="/model")

        # Setting up the model registry
        model_registry = new_controller_model_registry_basic_client()

        # Setting up the training pipeline
        train_pipeline = TrainingPipeline(
            model_name="forecast_model",
            data_source=data_source,
            data_transformer=data_transformer,
            model_destination=model_destination,
            model_generator=model_generator,
            model_validator=model_validator,
            model_registry=model_registry,
        )

        # Running the training pipeline
        train_pipeline.run()

    def predict(
        self,
        file_path: str,
        model_metadata: dict,
        start_date: str,
        end_date: str,
        interval_date_column: str = "start_of_quarter",
        time_travel: bool = False,
        time_travel_date: str = None,
        time_travel_date_column: str = "created_at",
        **kwargs, # Make it easier to add new parameters later but also bad.
    ):
        # Setting up the datasource
        data_source = LocalParquetDataSource(
            file_path=file_path,
            start_date=start_date,
            end_date=end_date,
            interval_date_column=interval_date_column,
            time_travel=time_travel,
            time_travel_date=time_travel_date,
            time_travel_date_column=time_travel_date_column,
        )

        # Setting up the transformer
        data_transformer = ForecastPredictDataTransformer()

        # Setting up the model source
        if (
            model_metadata["model_destination"]["location_type"] == "localfile"
        ):  # This way we can add other model sources later
            model_source = LocalFileModelSource(model_metadata=model_metadata)

        # Setting up the model registry
        model_registry = new_controller_model_registry_basic_client()

        # Setting up the data sink
        data_sink = LocalCsvDataSink(base_file_path="/output")

        # Setting up the prediction pipeline
        predict_pipeline = PredictPipeline(
            model_name="forecast_model",
            model_source=model_source,
            data_source=data_source,
            data_sink=data_sink,
            data_transformer=data_transformer,
            model_registry=model_registry,
        )

        # Running the prediction pipeline
        predict_pipeline.run()
