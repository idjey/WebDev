import os
import getpass
import netrc

NETRC_FILE = "_netrc"

# Checks if the _netrc file exists in the user's home directory, if not then create _netrc file in user's home directory
# Ask user to enter credentials and save them to _netrc file


def check_and_set_netrc_file():
    return os.path.exists(os.path.join(os.path.expanduser("~"), NETRC_FILE))


if not check_and_set_netrc_file():
    netrc_file = netrc.netrc(os.path.join(os.path.expanduser("~"), NETRC_FILE))
    username = input("Enter USERNAME: ")
    password = getpass.getpass("Enter PASSWORD: ")
    apitoken = getpass.getpass("Enter API TOKEN: ")
    netrc_file.add_machine(
        "https://hjf-bdw-stage.lkcompliant.net/", username, password, apitoken)
    print("Credentials saved to _netrc file.")

# Check if the user already exists in the _netrc file
    if username in netrc_file.hosts:
        print("User already exists in _netrc file.")
    else:
        print("Enter your credentials")
        username = input("Enter USERNAME: ")
        password = getpass.getpass("Enter PASSWORD: ")
        apitoken = getpass.getpass("Enter API TOKEN: ")
        netrc_file.add_machine(
            "https://hjf-bdw-stage.lkcompliant.net/", username, password, apitoken)
        print("Credentials saved to _netrc file.")


def get_credentials():
    if check_and_set_netrc_file():
        username, _, password = netrc.netrc(os.path.join(
            os.path.expanduser("~"), NETRC_FILE)).authenticators("https://hjf-bdw-stage.lkcompliant.net/")
        return username, password
    else:
        print("No _netrc file found.")
        return None, None



if __name__ == "__main__":
    check_and_set_netrc_file()
    username, password = get_credentials()
    print(f"Username: {username}")
    print(f"Machine: {NETRC_FILE}")
    print(f"Path: {os.path.join(os.path.expanduser('~'), NETRC_FILE)}")
    print(f"File exists: {check_and_set_netrc_file()}")





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
