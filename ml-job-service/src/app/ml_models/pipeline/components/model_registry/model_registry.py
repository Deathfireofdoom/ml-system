from abc import ABC, abstractmethod


class BaseModelRegistry(ABC):
    @abstractmethod
    def register_model(self, model_metadata: dict):
        pass


class ControllerModelRegistry(BaseModelRegistry):
    def __init__(self, controller_client):
        self.controller_client = controller_client

    def register_model(self, model_metadata: dict):
        self.controller_client.register_model(model_metadata)

    def register_run(self, run_metadata: dict):
        self.controller_client.register_run(run_metadata)


def new_controller_model_registry_basic_client():
    from app.services.controller_service import ControllerService
    from app.tools.env import env

    client = ControllerService(env.CONTROLLER_HOST, env.CONTROLLER_PORT)
    return ControllerModelRegistry(client)
