import requests
import subprocess
import logging
from config_manager import ConfigManager  # Assuming this is where your webdav_url is configured

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_webdav_connection(url):
    """Check connectivity to the WebDAV server."""
    try:
        response = requests.head(url)
        # 200 OK or 401 Unauthorized indicates the URL is reachable
        if response.status_code in [200, 401]:
            logger.info(f"Connection to {url} successful.")
            return True
        else:
            logger.error(f"Connection to {url} failed with status code: {response.status_code}.")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to {url}. Error: {e}")
        return False

def run_main():
    """Run the main.py script."""
    try:
        subprocess.run(['python', 'main.py', '--upload'], check=True)
        logger.info("main.py executed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"main.py execution failed: {e}")

if __name__ == "__main__":
    config = ConfigManager(default_config_path='config.json')
    webdav_url = config.get('webdav_url')

    if webdav_url and check_webdav_connection(webdav_url):
        run_main()
    else:
        logger.error("Skipping main.py execution due to connectivity issues.")
