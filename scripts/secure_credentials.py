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


def set_credentials():
    """Prompt user for credentials and set them as environment variables."""
    username = input("Enter your username: ")
    # Hides the password input
    password = getpass.getpass("Enter your password: ")

    # Set environment variables
    os.environ['WEBDAV_USERNAME'] = username
    os.environ['WEBDAV_PASSWORD'] = password

    print("Credentials set successfully.")


# Optionally, you could include a condition to automatically prompt for credentials
# if they are not found, but consider the security implications and user experience
if __name__ == "__main__":
    # Check if credentials are already set, if not, prompt the user
    try:
        get_credentials()
        print("Credentials are already set.")
    except ValueError:
        set_credentials()
