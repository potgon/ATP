import logging
import os
from logging.handlers import RotatingFileHandler
from utils.config import LOGS_DIR


def setup_logger(logger_name, log_file="dash.log", level=logging.INFO):
    """
    Set up a logger with a rotating file handler.

    Args:
        logger_name (str): Name of the logger.
        log_file (str): Name of the log file.
        level (int): Logging level. Default is logging.INFO.

    Returns:
        logging.Logger: Configured logger.
    """

    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    log_filepath = os.path.join(LOGS_DIR, log_file)
    handler = RotatingFileHandler(log_filepath, maxBytes=1e6, backupCount=5)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


# TODO make logger func
