import argparse
from etl_pipeline import run_pipeline, schedule_jobs
from webdev_utils import upload_to_webdev
from secure_credentials import check_and_set_netrc_file
from logging_config import setup_logging
from config_manager import ConfigManager
import os


def check_credentials():
    if 'WEBDAV_USERNAME' not in os.environ or 'WEBDAV_PASSWORD' not in os.environ:
        print("WEBDAV_USERNAME and WEBDAV_PASSWORD environment variables not set.")
        print("Please enter your WebDAV credentials:")
        username = input("Username: ")
        password = input("Password: ")
        os.environ['WEBDAV_USERNAME'] = username
        os.environ['WEBDAV_PASSWORD'] = password
        print("Credentials set.")
    else:
        print(
            "WEBDAV_USERNAME and WEBDAV_PASSWORD environment variables already set.")
        print("Using existing credentials.")
    return os.environ['WEBDAV_USERNAME'], os.environ['WEBDAV_PASSWORD']


def main(args):
    setup_logging()
    config = ConfigManager(default_config_path='config.json')

    if args.set_credentials:
        check_and_set_netrc_file()
    elif args.upload:
        print("Uploading files to WebDev")
        webdev_url = config.get('webdev_url')
        local_folder_path = config.get('local_folder_path')
        upload_to_webdev(webdev_url, local_folder_path)
    elif args.run_once:
        print("Running ETL pipeline once.")
        run_pipeline()
    else:
        print("Scheduling ETL pipeline.")
        schedule_jobs()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ETL Pipeline and Utilities Runner")
    parser.add_argument('--run-once', action='store_true',
                        help='Run the ETL pipeline once and exit.')
    parser.add_argument('--upload', action='store_true',
                        help='Upload files to WebDAV and exit.')
    parser.add_argument('--set-credentials', action='store_true',
                        help='Set up WebDAV credentials and store them in .env file.')

    args = parser.parse_args()
    main(args)
