import logging
import os
from logging.handlers import RotatingFileHandler
import pandas as pd
import subprocess

from utils.config import LOGS_DIR_PROD, LOGS_DIR_DEV


loggers = {}

def setup_logger(name: str, level: int, log_file: str) -> logging.Logger:
    log_env_dir = LOGS_DIR_PROD if get_current_git_branch() == "main" else LOGS_DIR_DEV
    if not os.path.exists(log_env_dir):
        os.makedirs(log_env_dir)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        log_path = os.path.join(log_env_dir, log_file)
        log_handler = RotatingFileHandler(log_path, maxBytes=1e6, backupCount=1)
        log_handler.setFormatter(formatter)
        log_handler.setLevel(level)
        logger.addHandler(log_handler)

    return logger


def make_log(name: str, level: int, log_file: str, msg):
    global loggers
    logger = loggers.get(name)

    log_levels = {
        10: logging.DEBUG,
        20: logging.INFO,
        30: logging.WARNING,
        40: logging.ERROR,
        50: logging.CRITICAL,
    }
    if not logger:
        logger = setup_logger(name, level, log_file)
        loggers[name] = logger

    log_level = log_levels.get(level, logging.DEBUG)
    logger.log(log_level, msg)


def log_full_dataframe(name: str, level: int, log_file: str, data: pd.DataFrame):
    """Logs whole dataframe by temporarily changing pandas settings to avoid data truncation

    Args:
        name (str): Logger instance name
        level (int): Logging level
        log_file (str): Log file name
        data (pd.DataFrame): DataFrame to log
    """

    original_max_rows = pd.get_option("display.max_rows")
    original_max_columns = pd.get_option("display.max_columns")
    original_width = pd.get_option("display.width")

    try:
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)

        make_log(name, level, log_file, f"DataFrame: \n {data}")

    finally:
        pd.set_option("display.max_rows", original_max_rows)
        pd.set_option("display.max_columns", original_max_columns)
        pd.set_option("display.width", original_width)

def get_current_git_branch():
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
        return branch
    except subprocess.CalledProcessError:
        return "unknown"
