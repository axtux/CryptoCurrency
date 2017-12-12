import logging

# CRITICAL ERROR WARNING INFO DEBUG
DEFAULT_LEVEL = logging.DEBUG
logger = None

def debug(message):
    global logger, DEFAULT_LEVEL
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(DEFAULT_LEVEL)
    logger.debug(message)

def warning(message):
    global logger, DEFAULT_LEVEL
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(DEFAULT_LEVEL)
    logger.warning(message)
