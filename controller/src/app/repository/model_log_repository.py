import json

from app.utils.db.db import get_db_cursor
from app.utils.logger.logger import get_logger

logger = get_logger()


class ModelLogRepostiory:
    def insert_log(
        self,
        model_name: str,
        model_version_id: str,
        model_metadata: dict,
    ):
        sql = """
            INSERT INTO model_log (model_name, version_id, metadata)
            VALUES (%s, %s, %s)
            """
        logger.info(f"Inserting model log for {model_name} {model_version_id}")
        values = (model_name, model_version_id, json.dumps(model_metadata))
        with get_db_cursor() as cursor:
            cursor.execute(sql, values)
        logger.info(f"Inserted model log for {model_name} {model_version_id}")

    def insert_pending_model(
        self,
        model_name: str,
        model_version_id: str,
        model_metadata: dict,
    ):
        sql = """
            INSERT INTO pending_models (model_name, version_id, metadata)
            VALUES (%s, %s, %s)
            """
        
        logger.info(f"Inserting pending model for {model_name} {model_version_id}")
        values = (model_name, model_version_id, json.dumps(model_metadata))
        with get_db_cursor() as cursor:
            cursor.execute(sql, values)
        logger.info(f"Inserted pending model for {model_name} {model_version_id}")

    def get_pending_model(self, model_name: str, model_version_id: str) -> dict:
        sql = """
            SELECT model_name, version_id, metadata
            FROM pending_models
            WHERE model_name = %s AND version_id = %s
            """
        
        logger.info(f"Getting pending model for {model_name} {model_version_id}")
        values = (model_name, model_version_id)
        with get_db_cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone()

    def get_model(self, model_name: str, model_version_id: str) -> dict:
        sql = """
            SELECT model_name, version_id, metadata
            FROM model_log
            WHERE model_name = %s AND version_id = %s
            """
        
        logger.info(f"Getting model for {model_name} {model_version_id}")
        values = (model_name, model_version_id)
        with get_db_cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone()

    def delete_pending_model(self, model_name: str, model_version_id: str):
        sql = """
            DELETE FROM pending_models
            WHERE model_name = %s AND version_id = %s
            """
        
        logger.info(f"Deleting pending model for {model_name} {model_version_id}")
        values = (model_name, model_version_id)
        with get_db_cursor() as cursor:
            cursor.execute(sql, values)
        logger.info(f"Deleted pending model for {model_name} {model_version_id}")

    def get_current_model(self, model_name: str) -> dict:
        sql = """
            SELECT model_name, version_id, metadata
            FROM current_production_model
            WHERE model_name = %s
            """
        
        logger.info(f"Getting current model for {model_name}")
        values = (model_name,)
        with get_db_cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone()
    
    def get_previous_model(self, model_name: str) -> dict:
        sql = """
            SELECT model_name, version_id, metadata
            FROM model_log
            WHERE model_name = %s
            ORDER BY created_at DESC
            LIMIT 1
            OFFSET 1
            """
        
        logger.info(f"Getting previous model for {model_name}")
        values = (model_name,)
        with get_db_cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone()
