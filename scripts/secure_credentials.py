import os
import getpass

def get_credentials():
    """Retrieves WebDAV credentials from environment variables or .env file."""
    load_dotenv()  # Ensure dotenv is loaded here as well to check for .env credentials
    username = os.environ.get('WEBDAV_USERNAME')
    password = os.environ.get('WEBDAV_PASSWORD')
    if not username or not password:
        print("Environment variables for WEBDAV_USERNAME or WEBDAV_PASSWORD are not set.")
        return None, None  # Return None to indicate missing credentials
    return username, password

def set_credentials_env():
    """Prompt for WebDAV credentials and save them to a .env file."""
    username = input("Enter WEBDAV_USERNAME: ")
    password = getpass.getpass("Enter WEBDAV_PASSWORD: ")  # Use getpass for secure password input
    
    env_path = os.path.join(os.getcwd(), '.env')  # Adjust path as needed
    with open(env_path, 'a') as env_file:  # 'a' to append to avoid overwriting existing content
        env_file.write(f"WEBDAV_USERNAME={username}\n")
        env_file.write(f"WEBDAV_PASSWORD={password}\n")
    
    print("Credentials saved to .env file.")

def load_dotenv():
    """Load .env file to environment variables if it exists."""
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

if __name__ == "__main__":
    load_dotenv()  # Ensure .env is loaded first
    username, password = get_credentials()
    if not username or not password:
        set_credentials_env()
    else:
        print("Credentials are already set.")
