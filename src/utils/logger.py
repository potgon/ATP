import logging
import os
from logging.handlers import RotatingFileHandler
import pandas as pd

from utils.config import LOGS_DIR


class DebugOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG


def setup_logger(name: str, level: int, log_file: str) -> logging.Logger:
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    logger = logging.getLogger(name)
    logger.setLevel(level)

    log_path = os.path.join(LOGS_DIR, log_file)
    log_handler = RotatingFileHandler(log_path, maxBytes=1e6, backupCount=5)
    log_handler.setFormatter(formatter)
    log_handler.setLevel(level)
    logger.addHandler(log_handler)

    return logger


def make_log(name: str, level: int, log_file: str, msg):
    log_levels = {
        10: logging.DEBUG,
        20: logging.INFO,
        30: logging.WARNING,
        40: logging.ERROR,
        50: logging.CRITICAL,
    }
    log_level = log_levels.get(level, logging.DEBUG)
    logger = setup_logger(name, log_level, log_file)
    logger.log(log_level, msg)


def setup_custom_logger(
    name: str, workflow_log="dash.log", price_data_log="price.log"
) -> logging.Logger:
    """Set up a logger with rotating file handlers for both workflow and price data logging.

    Args:
        name (str): Name of the logger.
        workflow_log (str): Name of the workflow log file. Default is "dash.log".
        price_data_log (str): Name of the price data log file. Default is "price.log".

    Returns:
        logging.Logger: Configured logger.
    """
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    workflow_log_path = os.path.join(LOGS_DIR, workflow_log)
    workflow_handler = RotatingFileHandler(
        workflow_log_path, maxBytes=1e6, backupCount=5
    )
    workflow_handler.setLevel(logging.INFO)
    workflow_handler.setFormatter(formatter)
    logger.addHandler(workflow_handler)

    price_data_log_path = os.path.join(LOGS_DIR, price_data_log)
    price_data_handler = RotatingFileHandler(
        price_data_log_path, maxBytes=1e6, backupCount=0
    )
    price_data_handler.setLevel(logging.DEBUG)
    price_data_handler.addFilter(DebugOnlyFilter())
    price_data_handler.setFormatter(formatter)
    logger.addHandler(price_data_handler)

    return logger


def log_full_dataframe(data: pd.DataFrame, logger: logging.Logger):
    """Logs whole dataframe by temporarily changing pandas settings to avoid data truncation

    Args:
        data (pd.DataFrame): Pandas DataFrame
        logger (logging.Logger): Logger instance
    """
    original_max_rows = pd.get_option("display.max_rows")
    original_max_columns = pd.get_option("display.max_columns")
    original_width = pd.get_option("display.width")

    try:
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)

        logger.debug(f"Updating graph, current data: \n {data}")

    finally:
        pd.set_option("display.max_rows", original_max_rows)
        pd.set_option("display.max_columns", original_max_columns)
        pd.set_option("display.width", original_width)
