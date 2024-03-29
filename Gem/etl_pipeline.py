
import os
import subprocess
import schedule
import time
from datetime import datetime
import json
import logging
from secure_credentials import get_credentials
from webdev_utils import upload_to_webdev
from logging_config import setup_logging  # Ensure this is your logging setup module
from config_manager import ConfigManager

# Ensure setup_logging is called at the beginning to configure logging properly
setup_logging()

# Load configuration using ConfigManager
config_path = 'config.json'  # Adjust if your configuration file is located elsewhere
config = ConfigManager(default_config_path=config_path)

def update_schedule_time(new_time_format='%H:%M'):
    """Updates the scheduled time for running the ETL pipeline in the configuration."""
    try:
        current_time = datetime.now().strftime(new_time_format)
        config.config['schedule_time'] = current_time
        config.save_config()  # Assuming ConfigManager has a method to save the updated config back to file
        logging.info(f"Updated schedule_time to {current_time} in {config_path}")
    except Exception as e:
        logging.error(f"Error updating configuration file: {e}")

def validate_config():
    """Ensures all required configuration keys are present for the ETL process."""
    required_keys = ['webdav_url', 'local_folder_path', 'log_folder', 'schedule_time', 'transformation_scripts']
    missing_keys = [key for key in required_keys if key not in config.config]
    if missing_keys:
        raise ValueError(f"Missing configuration for: {', '.join(missing_keys)}")
    logging.info("Configuration validated successfully.")

def run_transformation_script(script_path):
    """Executes a given transformation script from the configuration."""
    try:
        subprocess.run(['python', script_path], check=True)
        logging.info(f"Successfully processed {script_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing {script_path}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error executing {script_path}: {e}")

def run_pipeline():
    """Runs the data transformation scripts and uploads updated files to WebDAV."""
    logging.info("ETL Pipeline started")
    transformation_scripts = config.config.get('transformation_scripts', [])
    for script in transformation_scripts:
        run_transformation_script(script)
    
    webdav_url = config.config.get('webdav_url')
    local_folder_path = config.config.get('local_folder_path')
    if webdav_url and local_folder_path:
        upload_to_webdev(webdav_url, local_folder_path)
    else:
        logging.error("WebDAV URL or local folder path missing in configuration.")
    
    logging.info("ETL Pipeline finished")

def schedule_jobs():
    """Schedules the ETL pipeline to run at the specified time daily."""
    schedule_time = config.config.get('schedule_time')
    if schedule_time:
        schedule.every().day.at(schedule_time).do(run_pipeline)
        logging.info(f"Scheduled ETL pipeline to run daily at {schedule_time}.")
    else:
        logging.error("Schedule time not defined in configuration.")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    try:
        validate_config()
        schedule_jobs()
    except Exception as e:
        logging.critical(f"ETL pipeline initialization failed: {e}")



########################################
import os
import subprocess
import schedule
import time
from datetime import datetime
import json
import logging
from secure_credentials import get_credentials  # Ensure this is used correctly
from webdev_utils import upload_to_webdev  # Correct import based on the webdev_utils.py
from logging_config import setup_logging
from config_manager import ConfigManager

# Function to update the schedule_time in config.json
def update_schedule_time(config_path, new_time_format='%H:%M'):
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file {config_path} not found.")
        return
    current_time = datetime.now().strftime(new_time_format)
    config['schedule_time'] = current_time
    try:
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=4)
        logging.info(f"Updated schedule_time to {current_time} in {config_path}")
    except Exception as e:
        logging.error(f"Error updating configuration file: {e}")

# Load configuration and set up logging
config_file_path = 'config.json'
update_schedule_time(config_file_path)
config = ConfigManager(default_config_path=config_file_path)
setup_logging()

def validate_config():
    """Ensures all required configuration keys are present."""
    required_keys = ['webdav_url', 'local_folder_path', 'log_folder', 'schedule_time', 'transformation_scripts']
    missing_keys = [key for key in required_keys if not config.get(key)]
    if missing_keys:
        raise ValueError(f"Missing configuration for: {', '.join(missing_keys)}")

def run_transformation_script(script_path):
    """Executes a given transformation script and logs the outcome."""
    try:
        subprocess.run(['python', script_path], check=True)
        logging.info(f"Successfully processed {script_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing {script_path}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error executing {script_path}: {e}")

def run_pipeline():
    """Runs the data transformation scripts and uploads updated files to WebDAV."""
    logging.info("ETL Pipeline started")
    transformation_scripts = config.get('transformation_scripts')
    if transformation_scripts:
        for script in transformation_scripts:
            run_transformation_script(script)
    # Fetch credentials right before uploading
    credentials = get_credentials()
    if credentials:
        try:
            upload_to_webdev(config.get('webdav_url'), config.get('local_folder_path'), delay_seconds=60)
        except Exception as e:
            logging.error(f"Failed to upload files to WebDAV: {e}")
    else:
        logging.error("Credentials not found, unable to upload files.")
    logging.info("ETL Pipeline finished")

def schedule_jobs():
    """Schedules the ETL pipeline to run at a specified time daily."""
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
