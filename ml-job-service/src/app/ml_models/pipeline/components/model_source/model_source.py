from abc import ABC, abstractmethod


class BaseModelSource(ABC):
    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def get_model_metadata(self):
        pass

    @abstractmethod
    def get_model_version_identifier(self):
        pass


class LocalFileModelSource(BaseModelSource):
    def __init__(self, model_metadata: dict):
        self.model_metadata = model_metadata

    def load_model(self):
        from joblib import load

        return load(self.model_metadata["model_destination"]["file_path"])

    def get_model_metadata(self):
        return self.model_metadata

    def get_model_version_identifier(self):
        return self.model_metadata["model_destination"]["model_version_identifier"]
