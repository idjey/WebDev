import os
import getpass
import netrc

# Define the machine name for clearer reference
MACHINE_NAME = "https://hjf-bdw-stage.lkcompliant.net/"

def get_credentials():
    """Retrieves credentials from the _netrc file or prompts the user to enter them."""
    netrc_path = os.path.join(os.path.expanduser("~"), ".netrc")
    
    try:
        netrc_data = netrc.netrc(netrc_path)
    except FileNotFoundError:
        print("No .netrc file found. Please enter credentials to create one.")
        netrc_data = create_netrc(netrc_path)
    except netrc.NetrcParseError as e:
        print(f"Error parsing .netrc file: {e}")
        return None, None

    credentials = netrc_data.authenticators(MACHINE_NAME)
    if credentials:
        username, _, labkey_auth_token = credentials
        print("Credentials found in .netrc file.")
    else:
        print("No credentials found for the specified machine. Please enter new credentials.")
        username, labkey_auth_token = prompt_credentials()
        update_netrc(netrc_path, username, labkey_auth_token)

    return username, labkey_auth_token

def create_netrc(netrc_path):
    """Creates a new .netrc file with user credentials."""
    username, labkey_auth_token = prompt_credentials()
    try:
        with open(netrc_path, 'w') as netrc_file:
            netrc_file.write(f"machine {MACHINE_NAME}\n")
            netrc_file.write(f"login {username}\n")
            netrc_file.write(f"password {labkey_auth_token}\n")
        os.chmod(netrc_path, 0o600)  # Ensure the file is only accessible to the user
        print("Credentials saved to .netrc file.")
    except Exception as e:
        print(f"Error creating .netrc file: {e}")
        return None
    return netrc.netrc(netrc_path)

def prompt_credentials():
    """Prompts user for credentials and returns them."""
    username = input("Enter USERNAME: ")
    labkey_auth_token = getpass.getpass("Enter LabKey Auth Token: ")
    return username, labkey_auth_token

def update_netrc(netrc_path, username, labkey_auth_token):
    """Updates the .netrc file with new credentials."""
    try:
        with open(netrc_path, 'w') as netrc_file:
            netrc_file.write(f"machine {MACHINE_NAME}\n")
            netrc_file.write(f"login {username}\n")
            netrc_file.write(f"password {labkey_auth_token}\n")
        print("Credentials updated in .netrc file.")
    except Exception as e:
        print(f"Error updating .netrc file: {e}")

if __name__ == "__main__":
    username, labkey_auth_token = get_credentials()
    if username and labkey_auth_token:
        print(f"Username: {username}")
        print(f"LabKey Auth Token: {labkey_auth_token}")

############## _NETRC #################

import os
import getpass
import netrc

# Define the machine name for clearer reference
MACHINE_NAME = "https://hjf-bdw-stage.lkcompliant.net/"

def get_credentials():
    """Retrieves credentials from the _netrc file or prompts the user to enter them."""
    netrc_path = os.path.join(os.path.expanduser("~"), "_netrc")  # Changed to _netrc for Windows
    
    try:
        netrc_data = netrc.netrc(netrc_path)
    except FileNotFoundError:
        print("No _netrc file found. Please enter credentials to create one.")
        netrc_data = create_netrc(netrc_path)
    except netrc.NetrcParseError as e:
        print(f"Error parsing _netrc file: {e}")
        return None, None

    credentials = netrc_data.authenticators(MACHINE_NAME)
    if credentials:
        username, _, labkey_auth_token = credentials
        print("Credentials found in _netrc file.")
    else:
        print("No credentials found for the specified machine. Please enter new credentials.")
        username, labkey_auth_token = prompt_credentials()
        update_netrc(netrc_path, username, labkey_auth_token)

    return username, labkey_auth_token

def create_netrc(netrc_path):
    """Creates a new _netrc file with user credentials."""
    username, labkey_auth_token = prompt_credentials()
    try:
        with open(netrc_path, 'w') as netrc_file:
            netrc_file.write(f"machine {MACHINE_NAME}\n")
            netrc_file.write(f"login {username}\n")
            netrc_file.write(f"password {labkey_auth_token}\n")
        os.chmod(netrc_path, 0o600)  # Ensure the file is only accessible to the user
        print("Credentials saved to _netrc file.")
    except Exception as e:
        print(f"Error creating _netrc file: {e}")
        return None
    return netrc.netrc(netrc_path)

def prompt_credentials():
    """Prompts user for credentials and returns them."""
    username = input("Enter USERNAME: ")
    labkey_auth_token = getpass.getpass("Enter LabKey Auth Token: ")
    return username, labkey_auth_token

def update_netrc(netrc_path, username, labkey_auth_token):
    """Updates the _netrc file with new credentials."""
    try:
        with open(netrc_path, 'w') as netrc_file:
            netrc_file.write(f"machine {MACHINE_NAME}\n")
            netrc_file.write(f"login {username}\n")
            netrc_file.write(f"password {labkey_auth_token}\n")
        print("Credentials updated in _netrc file.")
    except Exception as e:
        print(f"Error updating _netrc file: {e}")

if __name__ == "__main__":
    username, labkey_auth_token = get_credentials()
    if username and labkey_auth_token:
        print(f"Username: {username}")
        print(f"LabKey Auth Token: {labkey_auth_token}")

