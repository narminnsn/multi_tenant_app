import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_event(message: str):
    logger.info(message)


def log_error(message: str, error: Exception):
    logger.error(f"{message}: {error}")
