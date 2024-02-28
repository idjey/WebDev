import os
import requests
from time import sleep
import logging
from urllib.parse import urljoin
from secure_credentials import get_credentials  # Correct usage based on secure_credentials.py

# Update the path according to your specific requirements or configurations
custom_certificate_path = r'C:\Users\path_to_certificates'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

def upload_to_webdev(webdav_url, local_folder_path, delay_seconds=60):
    """Uploads modified files to WebDAV, with improved error handling and logging."""
    username, password = get_credentials()
    if not username or not password:
        logger.error("Failed to get credentials for WebDAV upload.")
        return
    credentials = (username, password)
    files = os.listdir(local_folder_path)
    last_modified_times = {}
    file_hashes = {}

    for file_name in files:
        file_path = os.path.join(local_folder_path, file_name)
        if os.path.isfile(file_path) and file_changed(file_path, last_modified_times, file_hashes):
            try:
                with open(file_path, 'rb') as f:
                    upload_url = urljoin(webdav_url, os.path.basename(file_path))
                    response = requests.put(upload_url, data=f, auth=credentials, verify=custom_certificate_path)
                    response.raise_for_status()
                    logger.info(f"Successfully uploaded {file_name}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to upload {file_name}. Error: {e}")
            finally:
                sleep(delay_seconds)

######################################
def upload_to_webdev(webdav_url, local_folder_path, delay_seconds=60):
    """Uploads modified files to WebDAV, with improved error handling and logging."""
    username, password = get_credentials()
    if not username or not password:
        logger.error("Failed to get credentials for WebDAV upload.")
        return
    credentials = (username, password)
    files = os.listdir(local_folder_path)
    last_modified_times = {}
    file_hashes = {}

    for file_name in files:
        file_path = os.path.join(local_folder_path, file_name)
        if os.path.isfile(file_path) and file_changed(file_path, last_modified_times, file_hashes):
            try:
                with open(file_path, 'rb') as f:
                    # Ensure the webdav_url ends with a slash to correctly concatenate with the file name
                    if not webdav_url.endswith('/'):
                        webdav_url += '/'
                    upload_url = urljoin(webdav_url, os.path.basename(file_path))
                    response = requests.put(upload_url, data=f, auth=credentials, verify=custom_certificate_path)
                    response.raise_for_status()
                    logger.info(f"Successfully uploaded {file_name}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to upload {file_name}. Error: {e}")
            finally:
                sleep(delay_seconds)

######################################

if __name__ == "__main__":
    try:
        webdav_url = "https://yourwebdav.url/_webdav/Transformed_Data/%40files/Test_Folder/"
        local_folder_path = r"G:\CSV_DIRECT_UPLOAD"
        upload_to_webdev(webdav_url, local_folder_path)
    except Exception as e:
        logger.error(f"Failed in main execution: {e}")


######################################

import requests
from requests.auth import HTTPBasicAuth
import logging
from secure_credentials import get_credentials

# Assuming this is the path to your custom certificate
custom_certificate_path = r'C:\Users\ZscalerRootCertificate-2048-SHA256.crt'

def upload_to_webdev(webdav_url, local_folder_path, delay_seconds=60):
    username, password = get_credentials()
    if not username or not password:
        logging.error("Credentials not found or invalid.")
        return
    
    # Use the custom certificate path and basic auth for requests
    session = requests.Session()
    session.verify = custom_certificate_path
    session.auth = HTTPBasicAuth(username, password)

    files = os.listdir(local_folder_path)
    for file_name in files:
        file_path = os.path.join(local_folder_path, file_name)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'rb') as f:
                    upload_url = webdav_url + file_name  # Ensure this is the correct URL construction
                    response = session.put(upload_url, data=f)
                    response.raise_for_status()
                    logging.info(f"Successfully uploaded {file_name}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to upload {file_name}. Error: {e}")
            finally:
                time.sleep(delay_seconds)

