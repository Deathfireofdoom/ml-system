from abc import ABC, abstractmethod
from datetime import datetime
import os


class BaseDataSink(ABC):
    @abstractmethod
    def save_dataframe(self, df) -> dict:
        pass


class LocalCsvDataSink(BaseDataSink):
    def __init__(self, base_file_path: str):
        self.base_file_path = base_file_path

    def save_dataframe(self, df, model_name: str, run_id: str) -> dict:
        file_path = self._get_file_path(model_name, run_id)
        df.to_csv(file_path)
        return {
            "location_type": "localfile",
            "file_path": file_path,
            "run_id": run_id,
            "load_type": "csv",
        }

    def _get_file_path(self, model_name: str, run_id: str):
        date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = f"{self.base_file_path}/{model_name}/{date_string}"
        os.makedirs(folder, exist_ok=True)
        return f"{folder}/{run_id}.csv"
