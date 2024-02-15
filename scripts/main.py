import argparse
from etl_pipeline import run_pipeline, schedule_jobs
from webdev_utils import upload_to_webdav
from secure_credentials import set_credentials_env  # Updated to use the new function
from logging_config import setup_logging
from config_manager import ConfigManager

def main(args):
    setup_logging()
    config = ConfigManager(default_config_path='config.json')

    if args.set_credentials:
        set_credentials_env()  # Updated call
    elif args.upload:
        print("Uploading files to WebDAV.")
        webdav_url = config.get('webdav_url')
        local_folder_path = config.get('local_folder_path')
        upload_to_webdav(webdav_url, local_folder_path)
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
    parser.add_argument('--set-credentials', action='store_true', help='Set up WebDAV credentials and store them in .env file.')

    args = parser.parse_args()
    main(args)
