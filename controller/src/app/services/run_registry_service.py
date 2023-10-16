class RunRegistryService:
    def __init__(self, run_log_repository, pub_sub_client) -> None:
        self.repository = run_log_repository
        self.pub_sub_client = pub_sub_client

    def add_run(
        self,
        run_id: str,
        run_start_time: str,
        run_duration_ms: int,
        run_type: str,
        model_name: str,
        model_version_id: str,
        run_metadata: dict,
    ):
        self.repository.insert_log(
            run_id,
            run_start_time,
            run_duration_ms,
            run_type,
            model_name,
            model_version_id,
            run_metadata,
        )

        self.notify_subscribers_new_run(
            run_id,
            run_start_time,
            run_duration_ms,
            run_type,
            model_name,
            model_version_id,
            run_metadata,
        )

        if run_type == "prediction":
            self.notify_subscribers_new_output(
                model_name=model_name, run_metadata=run_metadata
            )

    def notify_subscribers_new_run(
        self,
        run_id,
        run_start_time,
        run_duration_ms,
        run_type,
        model_name,
        model_version_id,
        run_metadata,
    ):
        self.pub_sub_client.publish(
            "run_log",
            {
                "run_id": run_id,
                "run_start_time": run_start_time,
                "run_duration_ms": run_duration_ms,
                "run_type": run_type,
                "model_name": model_name,
                "model_version_id": model_version_id,
                "run_metadata": run_metadata,
            },
        )

    def notify_subscribers_new_output(self, model_name, run_metadata):
        self.pub_sub_client.publish(model_name, run_metadata)


def new_run_registry_service_with_redis_pub_sub():
    from app.utils.pub_sub.pub_sub import get_redis_client
    client = get_redis_client()

    from app.repository.run_log_repository import RunLogRepository
    run_log_repository = RunLogRepository()

    return RunRegistryService(
        run_log_repository=run_log_repository, pub_sub_client=client
    )
