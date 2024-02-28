import logging
import os
from logging.handlers import RotatingFileHandler
from config_manager import ConfigManager

def setup_logging():
    config = ConfigManager().config
    log_directory = config.get('log_folder', 'logs')
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    log_file_path = os.path.join(log_directory, 'application.log')
    
    # Basic logging setup
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    # Rotating file handler
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1024*1024*5, backupCount=5)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    logging.getLogger().addHandler(file_handler)

    logging.info("Logging setup complete.")



####################
import logging
import os
from logging.handlers import RotatingFileHandler
from config_manager import ConfigManager  # Assuming ConfigManager is the way configurations are managed

def setup_logging():
    # Load configuration using ConfigManager
    config = ConfigManager(default_config_path='config.json').config
    
    log_directory = config.get('log_folder', '.')  # Use '.' as default if 'log_folder' is not set
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
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Inform about logging setup completion
    logger.info("Logging setup complete.")
