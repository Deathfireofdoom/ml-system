from abc import ABC, abstractmethod
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from datetime import datetime


class BaseModelGenerator(ABC):
    """
    BaseModelGenerator is an abstract base class for creating and training a specific model.

    The train method should accept a pandas dataframe and return a trained model plus a dict with metadata about the
    training process.
    """

    @abstractmethod
    def train(self, X_train: pd.DataFrame, y_train: pd.DataFrame):
        pass

    @abstractmethod
    def get_run_metadata(self) -> dict:
        pass


class ForecastModelGenerator(BaseModelGenerator):
    def __init__(
        self,
        n_estimators: int = 500,
        min_impurity_decrease: float = 1e-4,
        min_samples_leaf: int = 30,
        max_samples: float = 0.7,
        n_jobs: int = 4,
    ):
        self.n_estimators = n_estimators
        self.min_impurity_decrease = min_impurity_decrease
        self.min_samples_leaf = min_samples_leaf
        self.max_samples = max_samples
        self.n_jobs = n_jobs

    def train(
        self, X_train: pd.DataFrame, y_train: pd.DataFrame
    ) -> RandomForestRegressor:
        model = self._get_model()

        start_time = datetime.now()
        model.fit(X_train, y_train)
        train_duration_milliseconds = (
            datetime.now() - start_time
        ).total_seconds() * 1000

        return model, self.get_run_metadata(
            train_duration_milliseconds=train_duration_milliseconds
        )

    def _get_model(self) -> RandomForestRegressor:
        return RandomForestRegressor(
            n_estimators=self.n_estimators,
            min_impurity_decrease=self.min_impurity_decrease,
            min_samples_leaf=self.min_samples_leaf,
            max_samples=self.max_samples,
            n_jobs=self.n_jobs,
        )

    def get_run_metadata(self, train_duration_milliseconds: float) -> dict:
        return {
            "train_duration_milliseconds": train_duration_milliseconds,
            "n_estimators": self.n_estimators,
            "min_impurity_decrease": self.min_impurity_decrease,
            "min_samples_leaf": self.min_samples_leaf,
            "max_samples": self.max_samples,
            "n_jobs": self.n_jobs,
        }
