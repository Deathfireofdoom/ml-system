from flask import Blueprint, jsonify
from flask import request

from app.utils.db.migrate import migrate_db
from app.utils.logger.logger import get_logger

logger = get_logger()

migrate = Blueprint("migrate", __name__)


@migrate.route("/", methods=["GET"])
def migrate_route():
    # Get version and direction from query parameters
    version = request.args.get("version")
    direction = request.args.get("direction", "up")



    # Check if version is provided
    if not version:
        return jsonify({"error": "Please provide a version"}), 400

    # Log the request
    logger.info(f"Got migrate request with version: {version} and direction: {direction}")

    try:
        # Call the migrate function with the provided version and direction
        migrate_db(version, direction)
        logger.info(f"Migration {version} {direction} executed successfully")
        return (
            jsonify(
                {"message": f"Migration {version} {direction} executed successfully"}
            ),
            200,
        )
    except Exception as e:
        # Log the exception for debugging purposes
        logger.error(f"Failed to execute migration {version} {direction}, {e}")
        return (
            jsonify(
                {"error": f"Failed to execute migration {version} {direction}, {e}"}
            ),
            500,
        )
