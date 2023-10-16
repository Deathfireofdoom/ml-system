from abc import ABC, abstractmethod
import numpy as np
from sklearn.metrics import mean_squared_error


class BaseModelValidator(ABC):
    """
    Validate a model, returns a dict with the results.
    """

    @abstractmethod
    def validate(self, model, X_test, y_test) -> dict:
        pass


class ForecastModelValidator(BaseModelValidator):
    def validate(self, model, X_test, y_test) -> dict:
        y_pred = self._predict(model, X_test)
        rmse = self._get_rmse(y_test, y_pred)
        return {"rmse": rmse}

    def _predict(self, model, X_test):
        return model.predict(X_test)

    def _get_rmse(self, y_true, y_pred):
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        return rmse
