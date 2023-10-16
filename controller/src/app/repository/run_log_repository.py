import json

from app.utils.db.db import get_db_cursor
from app.utils.logger.logger import get_logger

logger = get_logger()

class RunLogRepository:
    def insert_log(
        self,
        run_id: str,
        run_start_time: str,
        run_duration_ms: int,
        run_type: str,
        model_name: str,
        model_version_id: str,
        run_metadata: dict,
    ):
        sql = """
            INSERT INTO run_log (run_id, run_start_time, run_duration_ms, run_type, model_name, model_version_id, run_metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        values = (
            run_id,
            run_start_time,
            run_duration_ms,
            run_type,
            model_name,
            model_version_id,
            json.dumps(run_metadata),
        )

        logger.info(f"Inserting run log for {run_id}")
        with get_db_cursor() as cursor:
            cursor.execute(sql, values)
        logger.info(f"Inserted run log for {run_id}")

    def get_run(self, run_id: str) -> dict:
        sql = """
            SELECT run_id, run_start_time, run_duration_ms, run_type, model_name, model_version_id, run_metadata
            FROM run_log
            WHERE run_id = %s
            """
        values = (run_id,)

        logger.info(f"Getting run log for {run_id}")
        with get_db_cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone()
