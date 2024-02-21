import os
import getpass
import netrc

NETRC_FILE = "_netrc"

def get_credentials():
    """Retrieves credentials from the _netrc file or prompts the user to enter them."""
    netrc_path = os.path.join(os.path.expanduser("~"), NETRC_FILE)
    
    if not os.path.exists(netrc_path):
        print("No _netrc file found. Creating one.")
        try:
            netrc_file = netrc.netrc(netrc_path)
            username = input("Enter USERNAME: ")
            labkey_auth_token = getpass.getpass("Enter LabKey Auth Token: ")
            netrc_file.add_machine("https://hjf-bdw-stage.lkcompliant.net/", username=username, password=labkey_auth_token)
            print("Credentials saved to _netrc file.")
            return username, labkey_auth_token
        except Exception as e:
            print(f"Error creating _netrc file: {e}")
            return None, None

    try:
        netrc_file = netrc.netrc(netrc_path)
        username, _, labkey_auth_token = netrc_file.authenticators("https://hjf-bdw-stage.lkcompliant.net/")
        if username:
            print("Credentials already exist. Overwrite? (yes/no)")
            overwrite = input().strip().lower()
            if overwrite != 'yes':
                return username, labkey_auth_token
        new_username = input("Enter USERNAME: ")
        new_labkey_auth_token = getpass.getpass("Enter LabKey Auth Token: ")
        netrc_file.add_machine("https://hjf-bdw-stage.lkcompliant.net/", username=new_username, password=new_labkey_auth_token)
        print("Credentials saved to _netrc file.")
        return new_username, new_labkey_auth_token
    except Exception as e:
        print(f"Error retrieving or updating credentials from _netrc file: {e}")
        return None, None

if __name__ == "__main__":
    username, labkey_auth_token = get_credentials()
    if username:
        print(f"Username: {username}")
        print(f"LabKey Auth Token: {labkey_auth_token}")
        print(f"Machine: {NETRC_FILE}")
        print(f"Path: {os.path.join(os.path.expanduser('~'), NETRC_FILE)}")
        print(f"File exists: {os.path.exists(os.path.join(os.path.expanduser('~'), NETRC_FILE))}")

###############################
import os
import getpass
import netrc

NETRC_FILE = "_netrc"

def check_and_set_netrc_file():
    """Checks if the _netrc file exists in the user's home directory, if not then creates it."""
    netrc_path = os.path.join(os.path.expanduser("~"), NETRC_FILE)
    if not os.path.exists(netrc_path):
        print("No _netrc file found. Creating one.")
        try:
            netrc_file = netrc.netrc(netrc_path)
            username = input("Enter USERNAME: ")
            password = getpass.getpass("Enter PASSWORD: ")
            apitoken = getpass.getpass("Enter API TOKEN: ")
            netrc_file.add_machine("https://hjf-bdw-stage.lkcompliant.net/", username, password, apitoken)
            print("Credentials saved to _netrc file.")
        except Exception as e:
            print(f"Error creating _netrc file: {e}")

def get_credentials():
    """Retrieves credentials from the _netrc file."""
    netrc_path = os.path.join(os.path.expanduser("~"), NETRC_FILE)
    if os.path.exists(netrc_path):
        try:
            netrc_file = netrc.netrc(netrc_path)
            username, _, password = netrc_file.authenticators("https://hjf-bdw-stage.lkcompliant.net/")
            return username, password
        except Exception as e:
            print(f"Error retrieving credentials from _netrc file: {e}")
    else:
        print("No _netrc file found.")
    return None, None

def update_credentials():
    """Updates credentials in the _netrc file."""
    netrc_path = os.path.join(os.path.expanduser("~"), NETRC_FILE)
    if os.path.exists(netrc_path):
        try:
            netrc_file = netrc.netrc(netrc_path)
            if "https://hjf-bdw-stage.lkcompliant.net/" in netrc_file.hosts:
                username = input("Enter new USERNAME: ")
                password = getpass.getpass("Enter new PASSWORD: ")
                apitoken = getpass.getpass("Enter new API TOKEN: ")
                netrc_file.add_machine("https://hjf-bdw-stage.lkcompliant.net/", username, password, apitoken)
                print("Credentials updated in _netrc file.")
            else:
                print("No existing credentials found for the specified machine.")
        except Exception as e:
            print(f"Error updating credentials in _netrc file: {e}")
    else:
        print("No _netrc file found.")

def delete_credentials():
    """Deletes credentials for the specified machine from the _netrc file."""
    netrc_path = os.path.join(os.path.expanduser("~"), NETRC_FILE)
    if os.path.exists(netrc_path):
        try:
            netrc_file = netrc.netrc(netrc_path)
            if "https://hjf-bdw-stage.lkcompliant.net/" in netrc_file.hosts:
                del netrc_file.hosts["https://hjf-bdw-stage.lkcompliant.net/"]
                print("Credentials deleted from _netrc file.")
            else:
                print("No existing credentials found for the specified machine.")
        except Exception as e:
            print(f"Error deleting credentials from _netrc file: {e}")
    else:
        print("No _netrc file found.")

if __name__ == "__main__":
    check_and_set_netrc_file()
    username, password = get_credentials()
    print(f"Username: {username}")
    print(f"Machine: {NETRC_FILE}")
    print(f"Path: {os.path.join(os.path.expanduser('~'), NETRC_FILE)}")
    print(f"File exists: {os.path.exists(os.path.join(os.path.expanduser('~'), NETRC_FILE))}")




##########################
import os
import getpass
import netrc

NETRC_FILE = "_netrc"


def check_netrc_file():
    """Checks if the _netrc file exists in the user's home directory."""
    return os.path.exists(os.path.join(os.path.expanduser("~"), NETRC_FILE))


def get_credentials():
    """Retrieves WebDAV credentials from _netrc file."""
    try:
        secrets = netrc.netrc(os.path.expanduser("~"), NETRC_FILE)
        username, _, password = secrets.authenticators("https://hjf-bdw-stage.lkcompliant.net/_webdav/Transformed_Data/@files/")
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
        # Replace "example.com" with your WebDAV server
        netrc_file.write(f"machine example.com login {
                         username} password {password}\n")

    print("Credentials saved to _netrc file.")


if __name__ == "__main__":
    if not check_netrc_file():
        set_credentials_netrc()
    else:
        print("Credentials already set.")


# import os
# import getpass


# def get_credentials():
#     """Retrieves WebDAV credentials from environment variables."""
#     username = os.environ.get('WEBDAV_USERNAME')
#     password = os.environ.get('WEBDAV_PASSWORD')
#     if not username or not password:
#         raise ValueError(
#             "Environment variables for WEBDAV_USERNAME or WEBDAV_PASSWORD are not set.")
#     return username, password


# def set_credentials():
#     """Prompt user for credentials and set them as environment variables."""
#     username = input("Enter your username: ")
#     # Hides the password input
#     password = getpass.getpass("Enter your password: ")

#     # Set environment variables
#     os.environ['WEBDAV_USERNAME'] = username
#     os.environ['WEBDAV_PASSWORD'] = password

#     print("Credentials set successfully.")


# # Optionally, you could include a condition to automatically prompt for credentials
# # if they are not found, but consider the security implications and user experience
# if __name__ == "__main__":
#     # Check if credentials are already set, if not, prompt the user
#     try:
#         get_credentials()
#         print("Credentials are already set.")
#     except ValueError:
#         set_credentials()
