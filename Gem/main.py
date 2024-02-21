import argparse
import schedule
import time
import logging
from secure_credentials import get_credentials, set_credentials_netrc
from webdev_utils import upload_to_webdev

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(args):
    if args.set_credentials:
        set_credentials_netrc()
    elif args.upload:
        logger.info("Uploading files to WebDev")
        # Replace with your WebDAV URL
        webdav_url = "https://hjf-bdw-stage.lkcompliant.net/_webdav/Transformed_Data/@files/"
        local_folder_path = "test_files"  # Replace with your local folder path
        upload_to_webdev(webdav_url, local_folder_path)
    elif args.run_once:
        logger.info("Running ETL pipeline once.")
        # Call function to run ETL pipeline
    else:
        logger.info("Scheduling ETL pipeline.")
        # Schedule jobs for ETL pipeline


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ETL Pipeline and Utilities Runner")
    parser.add_argument('--run-once', action='store_true',
                        help='Run the ETL pipeline once and exit.')
    parser.add_argument('--upload', action='store_true',
                        help='Upload files to WebDAV and exit.')
    parser.add_argument('--set-credentials', action='store_true',
                        help='Set up WebDAV credentials and store them in _netrc file.')
    args = parser.parse_args()

    main(args)
