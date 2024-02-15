import os
import requests
from time import sleep
import logging
from urllib.parse import urljoin
# Use centralized credential management
from secure_credentials import get_credentials
from config import config  # Assuming SSL cert path and other configs are here
from logging_config import setup_logging  # Centralized logging configuration
from dotenv import load_dotenv

load_dotenv()

setup_logging()  # Initialize logging based on centralized configuration


def file_hash(file_path):
    """Generates an MD5 hash for a file. Useful for detecting changes."""
    import hashlib
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def file_changed(file_path, last_modified_times, file_hashes):
    """Determines if a file has changed based on its hash and modification time."""
    current_hash = file_hash(file_path)
    last_modified = os.path.getmtime(file_path)
    if file_path not in file_hashes or file_hashes[file_path] != current_hash or last_modified_times.get(file_path, 0) < last_modified:
        file_hashes[file_path] = current_hash
        last_modified_times[file_path] = last_modified
        return True
    return False


def upload_to_webdav(webdav_url, local_folder_path, delay_seconds=60):
    """Uploads modified files to WebDAV, with improved error handling and logging."""
    credentials = get_credentials()  # Retrieve credentials at the point of use
    files = os.listdir(local_folder_path)
    last_modified_times = {}
    file_hashes = {}

    for file in files:
        file_path = os.path.join(local_folder_path, file)
        if os.path.isfile(file_path) and file_changed(file_path, last_modified_times, file_hashes):
            try:
                with open(file_path, 'rb') as f:
                    upload_url = urljoin(
                        webdav_url, os.path.basename(file_path))
                    response = requests.put(
                        upload_url, data=f, auth=credentials, verify=False )#config['custom_certificate_path'])
                    response.raise_for_status()  # Ensures HTTP errors are caught
                    logging.info(f"Successfully uploaded {file}")
            except requests.exceptions.RequestException as e:  # Catches all HTTP-related exceptions
                logging.error(f"Failed to upload {file}. Error: {e}")
            finally:
                # Avoids overloading the server with rapid uploads
                sleep(delay_seconds)


if __name__ == "__main__":
    try:
        setup_logging()  # Ensure logging is configured at the start
        webdav_url = config['webdav_url']
        local_folder_path = config['local_folder_path']
        upload_to_webdav(webdav_url, local_folder_path)
    except Exception as e:
        logging.error(f"Failed in main execution: {e}")
