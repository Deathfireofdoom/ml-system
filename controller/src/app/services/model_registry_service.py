from app.utils.logger.logger import get_logger
from app.config.evalute_criterias import EVALUATE_CRITERIAS

log = get_logger()


class ModelRegistryService:
    def __init__(self, model_log_repository, pub_sub_client) -> None:
        self.repository = model_log_repository
        self.pub_sub_client = pub_sub_client
        self.evalute_criterias = EVALUATE_CRITERIAS # NOTE: Not nicest way to do this.

    def add_run(self, model_name: str, model_version_id: str, model_metadata: dict):
        promote = self._evaluate_model(model_name, model_metadata)
        if promote:
            self.add_model(model_name, model_version_id, model_metadata)
        else:
            self.add_pending_model(model_name, model_version_id, model_metadata)

    def add_model(self, model_name: str, model_version_id: str, model_metadata: dict):
        self.repository.insert_log(model_name, model_version_id, model_metadata)
        self.notify_subscribers_new_model(model_name, model_version_id, model_metadata)

    def notify_subscribers_new_pending_model(
        self, model_name, model_version_id, model_metadata
    ):
        self.pub_sub_client.publish(
            "pending_model_log",
            {
                "model_name": model_name,
                "model_version_id": model_version_id,
                "model_metadata": model_metadata,
            },
        )

    def add_pending_model(
        self, model_name: str, model_version_id: str, model_metadata: dict
    ):
        self.repository.insert_pending_model(
            model_name, model_version_id, model_metadata
        )
        self.notify_subscribers_new_pending_model(
            model_name, model_version_id, model_metadata
        )

    def notify_subscribers_new_model(
        self, model_name, model_version_id, model_metadata
    ):
        self.pub_sub_client.publish(
            "model_log",
            {
                "model_name": model_name,
                "model_version_id": model_version_id,
                "model_metadata": model_metadata,
            },
        )

    def _evaluate_model(self, model_name: str, model_metadata: dict):
        evaluation_criteria = self.evalute_criterias[model_name]
        try:
            validation_results = model_metadata["model_metrics"]
        except Exception:
            raise Exception(f"validation_results not {model_metadata}")

        for metric, criteria in evaluation_criteria.items():
            if metric not in validation_results:
                log.error(f"metric {metric} not in validation_results")
                log.info(f"Model is not promoted")
                return False
            _max = criteria.get("max")
            if _max:
                if _max < validation_results[metric]:
                    log.warning(f"metric {metric} is {validation_results[metric]} but should be below {_max}")
                    log.info(f"Model is not promoted")
                    return False

            _min = criteria.get("min")
            if _min:
                if _min > validation_results[metric]:
                    log.warning(f"metric {metric} is {validation_results[metric]} but should be above {_min}")
                    log.info(f"Model is not promoted")
                    return False
                
        log.info(f"Model {model_name} is promoted with {model_metadata}")
        return True

    def promote_model(self, model_name: str, model_version_id: str):
        # checks if model is pending
        model = self.repository.get_pending_model(model_name, model_version_id)

        if not model:
            model = self.repository.get_model(model_name, model_version_id)

        # add model
        self.add_model(
            model_name=model[0],
            model_version_id=model[1],
            model_metadata=model[2],
        )

        # delete pending model
        self.repository.delete_pending_model(model_name, model_version_id)

    def demote_model(self, model_name: str):
        # get the previous promoted model
        previous_model = self.repository.get_previous_model(model_name)

        # promote the previous model
        self.add_model(
            model_name=previous_model[0],
            model_version_id=previous_model[1],
            model_metadata=previous_model[2],
        )


def new_model_registry_service_with_redis_pub_sub():
    from app.utils.pub_sub.pub_sub import get_redis_client
    client = get_redis_client()

    from app.repository.model_log_repository import ModelLogRepostiory
    model_log_repository = ModelLogRepostiory()

    return ModelRegistryService(
        model_log_repository=model_log_repository, pub_sub_client=client
    )
