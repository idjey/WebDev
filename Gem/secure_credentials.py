
----------------------------
|  GPT
----------------------------

import os
import getpass
import netrc

NETRC_FILE = "_netrc"

def get_credentials():
    """Retrieves WebDAV credentials from _netrc file."""
    try:
        secrets = netrc.netrc(os.path.expanduser("~"), NETRC_FILE)
        username, _, password = secrets.authenticators("example.com")  # Replace "example.com" with your WebDAV server
        return username, password
    except (FileNotFoundError, TypeError):
        print("Failed to retrieve credentials from _netrc file.")
        return None, None

def set_credentials_netrc():
    """Prompt for WebDAV credentials and save them to _netrc file."""
    username = input("Enter WEBDAV_USERNAME: ")
    password = getpass.getpass("Enter WEBDAV_PASSWORD: ")

    netrc_path = os.path.join(os.path.expanduser("~"), NETRC_FILE)
    with open(netrc_path, 'a') as netrc_file:
        netrc_file.write(f"machine example.com login {username} password {password}\n")  # Replace "example.com" with your WebDAV server

    print("Credentials saved to _netrc file.")

if __name__ == "__main__":
    username, password = get_credentials()
    if not username or not password:
        set_credentials_netrc()
    else:
        print("Credentials already set.")

----------------------------
|  GEMINI
----------------------------

import os
import getpass
from netrc import netrc

def get_credentials():
    """Retrieves WebDAV credentials securely from _netrc or prompts the user."""
    home_dir = os.path.expanduser("~")  # Get the user's home directory
    netrc_path = os.path.join(home_dir, '_netrc')

    try:
        # Load credentials from _netrc
        netrc_data = netrc(netrc_path) 
        username, _, password = netrc_data.authenticators("machine_name")  # Replace 'machine_name' with your WebDAV hostname
        return username, password

    except FileNotFoundError:
        print(".netrc file not found. Please follow the instructions below to create one.")
    except netrc.NetrcParseError:
        print("Error parsing .netrc file. Please ensure it has the correct format.")

    # Prompt the user if credentials aren't found in _netrcprint("WebDAV credentials not found in _netrc.")  
    username = input("Enter WEBDAV_USERNAME: ")
    password = getpass.getpass("Enter WEBDAV_PASSWORD: ")
    return username, password
