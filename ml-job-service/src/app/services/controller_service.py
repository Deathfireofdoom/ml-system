import requests


class ControllerService:
    def __init__(self, host: str, port: str):
        self.url = f"http://{host}:{port}"

    def register_model(self, model_metadata: dict):
        url = f"{self.url}/model/register"
        response = requests.post(url, json=model_metadata)
        if response.status_code != 200:
            raise Exception(f"Error registering model: {response.text} {url}")
        return response.json()

    def register_run(self, run_metadata: dict):
        url = f"{self.url}/run/register"
        response = requests.post(url, json=run_metadata)
        if response.status_code != 200:
            raise Exception(f"Error registering run: {response.text} {url}")
        return response.json()
