import os
import getpass


def get_credentials():
    """Retrieves WebDAV credentials from environment variables."""
    username = os.environ.get('WEBDAV_USERNAME')
    password = os.environ.get('WEBDAV_PASSWORD')
    if not username or not password:
        raise ValueError(
            "Environment variables for WEBDAV_USERNAME or WEBDAV_PASSWORD are not set.")
    return username, password

import os

def set_credentials_env():
    """Prompt for WebDAV credentials and save them to a .env file."""
    username = input("Enter WEBDAV_USERNAME: ")
    password = input("Enter WEBDAV_PASSWORD: ")
    
    env_path = os.path.join(os.getcwd(), '.env')  # Adjust path as needed
    with open(env_path, 'a') as env_file:  # 'a' to append to avoid overwriting existing content
        env_file.write(f"WEBDAV_USERNAME={username}\n")
        env_file.write(f"WEBDAV_PASSWORD={password}\n")
    
    print("Credentials saved to .env file.")


# Optionally, you could include a condition to automatically prompt for credentials
# if they are not found, but consider the security implications and user experience
if __name__ == "__main__":
    # Check if credentials are already set, if not, prompt the user
    try:
        get_credentials()
        print("Credentials are already set.")
    except ValueError:
        set_credentials()
