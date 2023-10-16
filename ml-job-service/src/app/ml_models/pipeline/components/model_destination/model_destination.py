from abc import ABC, abstractmethod
from joblib import dump
import os


class BaseModelDestination(ABC):
    """
    Base class for model destinations which can be used to save the model to different locations.
    A model destination can be a local file, a database, a remote file, etc.

    The save_model method should save the model to the specified location and return a dict
    with info about location and method of saving.
    """

    @abstractmethod
    def save_model(self, model) -> dict:
        pass


class LocalFileModelDestination(BaseModelDestination):
    def __init__(self, base_file_path: str):
        self.base_file_path = base_file_path

    def save_model(
        self, model, model_name: str, model_version_identifier: str = None
    ) -> dict:
        if not model_version_identifier:
            model_version_identifier = self._get_identifier()

        file_path = self._get_file_path(model_name, model_version_identifier)
        dump(model, file_path)
        return {
            "location_type": "localfile",
            "file_path": file_path,
            "model_version_identifier": model_version_identifier,
            "load_type": "joblib",
        }

    def _get_file_path(self, model_name: str, model_version_identifier: str = None):
        folder = f"{self.base_file_path}/{model_name}"
        os.makedirs(folder, exist_ok=True)
        return f"{folder}/{model_version_identifier}.joblib"
