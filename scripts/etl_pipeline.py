import os
import subprocess
import schedule
import time
from datetime import datetime
import json
import logging
from secure_credentials import get_credentials
from webdev_utils import upload_to_webdav
from logging_config import setup_logging
from config_manager import ConfigManager

# Function to update the schedule_time in config.json


def update_schedule_time(config_path, new_time_format='%H:%M'):
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file {config_path} not found.")
        return
    current_time = datetime.now().strftime(new_time_format)
    config['schedule_time'] = current_time
    try:
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=4)
        print(f"Updated schedule_time to {current_time} in {config_path}")
    except Exception as e:
        print(f"Error updating configuration file: {e}")


# Update schedule time before loading configuration
# Ensure this path is correct and consistent
config_file_path = r'config.json'
update_schedule_time(config_file_path)

# Load configuration and set up logging
config = ConfigManager(default_config_path=config_file_path)
setup_logging()


def validate_config():
    """Ensures all required configuration keys are present."""
    required_keys = ['webdav_url', 'local_folder_path',
                     'log_folder', 'schedule_time', 'transformation_scripts']
    missing_keys = [key for key in required_keys if config.get(key) is None]
    if missing_keys:
        raise ValueError(f"Missing configuration for: {
                         ', '.join(missing_keys)}")


def run_transformation_script(script_path):
    """Executes a given transformation script and logs the outcome, improved error handling."""
    try:
        subprocess.run(['python', script_path], check=True)
        logging.info(f"Successfully processed {script_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing {script_path}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error executing {script_path}: {e}")


def run_pipeline():
    """Runs the data transformation scripts and uploads updated files to WebDAV, with better logging."""
    logging.info("ETL Pipeline started")
    transformation_scripts = config.get('transformation_scripts')
    if transformation_scripts:
        for script in transformation_scripts:
            run_transformation_script(script)

    try:
        upload_to_webdav(config.get('webdav_url'), config.get(
            'local_folder_path'), get_credentials())
    except Exception as e:
        logging.error(f"Failed to upload files to WebDAV: {e}")

    logging.info("ETL Pipeline finished")


def schedule_jobs():
    """Schedules the ETL pipeline to run at a specified time daily, with robust error handling."""
    schedule_time = config.get('schedule_time')
    if schedule_time:
        schedule.every().day.at(schedule_time).do(run_pipeline)

    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logging.error(f"Error during scheduled job: {e}")
        time.sleep(60)


if __name__ == "__main__":
    try:
        validate_config()
        schedule_jobs()
    except Exception as e:
        logging.critical(f"ETL pipeline initialization failed: {e}")
