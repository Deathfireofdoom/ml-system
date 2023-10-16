import logging

from app.utils.env.env import env

log = logging.getLogger()
log.setLevel(env.LOG_LEVEL)


def get_logger():
    """returns a shared logger instance."""
    return log
