import logging
import os
from logging.handlers import RotatingFileHandler
from config import config


def setup_logging():
    log_directory = config.get('log_folder', '.')
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_file_path = os.path.join(log_directory, 'application.log')

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=1024*1024*5, backupCount=5)  # 5 MB per file, keep 5 backups
    console_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    log_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
