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
