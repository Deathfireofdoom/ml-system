from app.utils.db.db import get_db_cursor
from pathlib import Path


def migrate_db(version: str, direction: str = True):
    # Get the path to the migration scripts - not 100% happy with this
    current_directory = Path(__file__).parent
    migrate_folder_path = current_directory / "migrate"

    # Load the migration scripts
    file_name = f"{version}_{direction}.sql"

    if not migrate_folder_path / file_name:
        raise ValueError(f"Migration script {file_name} does not exist.")

    with open(migrate_folder_path / file_name, "r") as f:
        sql = f.read()

    # Execute the migration script
    with get_db_cursor() as cursor:
        cursor.execute(sql)
