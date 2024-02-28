import argparse
from etl_pipeline import run_pipeline, schedule_jobs
from webdev_utils import upload_to_webdev
from secure_credentials import get_credentials  # Assuming this is still relevant
from logging_config import setup_logging
from config_manager import ConfigManager

def main():
    setup_logging()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="ETL Pipeline and WebDAV Utilities Runner")
    parser.add_argument('--run-once', action='store_true', help='Run the ETL pipeline once and exit.')
    parser.add_argument('--upload', action='store_true', help='Upload files to WebDAV and exit.')
    parser.add_argument('--set-credentials', action='store_true', help='Interactively set or update credentials.')
    args = parser.parse_args()

    config = ConfigManager(default_config_path='config.json')

    if args.set_credentials:
        # Example function to interactively set credentials - you might need to implement this
        print("Setting or updating credentials is not directly supported in this script.")
    elif args.upload:
        webdav_url = config.get('webdav_url')
        local_folder_path = config.get('local_folder_path')
        if webdav_url and local_folder_path:
            print("Uploading files to WebDAV")
            upload_to_webdev(webdav_url, local_folder_path)
        else:
            print("WebDAV URL or local folder path is not configured properly.")
    elif args.run_once:
        print("Running ETL pipeline once.")
        run_pipeline()
    else:
        print("Scheduling ETL pipeline to run at configured intervals.")
        schedule_jobs()

if __name__ == "__main__":
    main()


###########################################
import argparse
from etl_pipeline import run_pipeline, schedule_jobs
from webdev_utils import upload_to_webdev
from secure_credentials import get_credentials  # Corrected import based on secure_credentials.py
from logging_config import setup_logging
from config_manager import ConfigManager

def main(args):
    setup_logging()
    config = ConfigManager(default_config_path='config.json')

    if args.set_credentials:
        # Since there's no direct method named check_and_set_netrc_file, we'll call get_credentials()
        username, _ = get_credentials()
        if username:
            print("Credentials confirmed or set.")
        else:
            print("Failed to confirm or set credentials.")
    elif args.upload:
        print("Uploading files to WebDev")
        webdev_url = config.get('webdev_url')
        local_folder_path = config.get('local_folder_path')
        # Credentials will be fetched inside the upload_to_webdev function
        upload_to_webdev(webdev_url, local_folder_path)
    elif args.run_once:
        print("Running ETL pipeline once.")
        run_pipeline()
    else:
        print("Scheduling ETL pipeline.")
        schedule_jobs()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL Pipeline and Utilities Runner")
    parser.add_argument('--run-once', action='store_true', help='Run the ETL pipeline once and exit.')
    parser.add_argument('--upload', action='store_true', help='Upload files to WebDAV and exit.')
    parser.add_argument('--set-credentials', action='store_true', help='Prompt to set up WebDAV credentials in the _netrc file.')

    args = parser.parse_args()
    main(args)
