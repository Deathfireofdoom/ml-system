from abc import ABC, abstractmethod
from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split


class BaseDataTransformer(ABC):
    """
    BaseDataTransformer is an abstract base class for data transformers. This class separates the concern of
    transforming the data. This is useful because we can easily swap out the data transformer for another one.

    The transform method should accept a pandas dataframe and return a tuple of 4 pandas dataframes,
    The dataframe should be split into 4 parts:
    - X_train
    - X_test
    - y_train
    - y_test

    Notes
    -----
    This is can feel like a uncessary abstraction for this project, since the transformation is very simple. In a real
    world scenario the transformation can be more complex.

    However, on that note, I also do believe the transformation should be done in a separate process if possible, like
    a ETL pipeline into a feature store.
    """

    @abstractmethod
    def transform(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        pass


class ForecastTrainDataTransformer(BaseDataTransformer):
    """
    This is a datatransformer for the forecasting pipeline, the assignment.

    I am not sure if I am happy with the "non"-modular design of this class, on one hand this class should only
    be used for a specific pipeline, but on the other hand it goes against the rest of the design where I try to
    make everything as modular as possible.

    But limited time and all that, I will not put too much effort into that thought right now.
    """

    def __init__(self, test_size: float = 0.2, random_state: int = 42) -> None:
        self.test_size = test_size
        self.random_state = random_state

    def transform(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Transforms the data into a format that can be used for forecasting.
        """
        X = self._get_features(df)
        y = self._get_target(df)

        X_train, X_test, y_train, y_test = self._split_data(X, y)

        return X_train, X_test, y_train, y_test

    @staticmethod
    def _get_features(df: pd.DataFrame) -> pd.DataFrame:
        # extract the features we want to have as independent variables
        df = df[["cloudcover_low", "cloudcover_mid", "cloudcover_high"]].assign(
            hour=lambda df: df.index.hour.astype("float"),
            month=lambda df: df.index.month.astype("float"),
            minutes=lambda df: 60.0 * df.index.hour + df.index.minute,
            day=lambda df: df.index.dayofyear.astype("float"),
        )
        return df

    @staticmethod
    def _get_target(df: pd.DataFrame) -> pd.DataFrame:
        # extract the target variable
        df = df["power"]
        return df

    def _split_data(self, X: pd.DataFrame, y: pd.DataFrame) -> pd.DataFrame:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, shuffle=True
        )

        return X_train, X_test, y_train, y_test


class ForecastPredictDataTransformer(BaseDataTransformer):
    def transform(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        index = df.index
        X = self._get_features(df)
        return index, X

    @staticmethod
    def _get_features(df: pd.DataFrame) -> pd.DataFrame:
        # extract the features we want to have as independent variables
        df = df[["cloudcover_low", "cloudcover_mid", "cloudcover_high"]].assign(
            hour=lambda df: df.index.hour.astype("float"),
            month=lambda df: df.index.month.astype("float"),
            minutes=lambda df: 60.0 * df.index.hour + df.index.minute,
            day=lambda df: df.index.dayofyear.astype("float"),
        )
        return df
