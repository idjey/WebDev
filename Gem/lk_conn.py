from labkey.api_wrapper import APIWrapper

# Configuration for APIWrapper - replace with your actual details
labkey_server = 'your_labkey_server_address'  # e.g., 'www.labkey.org'
project_name = 'YourProjectName'  # e.g., 'Project/Folder/Subfolder'
contextPath = 'labkey'  # Adjust based on your server's context path, if any
schema = 'core'  # Example schema
table = 'Users'  # Example table to query

# Initialize the APIWrapper
api = APIWrapper(domain=labkey_server,
                 container_path=project_name,
                 context_path=contextPath,
                 use_ssl=True,  # Set to True if your LabKey server uses SSL
                 verify_ssl=False,  # Set to False only for development servers with self-signed certificates
                 api_key='your_api_key_here',  # Optional: Use if not using a netrc file
                 disable_csrf=False)  # Keep as False unless you have a specific reason to disable CSRF protection

# Example operation using APIWrapper
def query_users():
    try:
        result = api.query.select_rows(schema, table)
        if result and 'rows' in result:
            print("select_rows: Number of rows returned:", str(result['rowCount']))
            for row in result['rows']:
                print(row)
        else:
            print('select_rows: Failed to load results from', schema, '.', table)
    except Exception as e:
        print('An error occurred:', e)

if __name__ == "__main__":
    query_users()
