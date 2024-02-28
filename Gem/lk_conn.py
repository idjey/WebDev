from labkey.api_wrapper import APIWrapper
from config_manager import ConfigManager

# Load configuration
config = ConfigManager().config

labkey_server = config.get('labkey_server', 'localhost:8080')
project_name = config.get('labkey_project_name', 'Project/Folder/Subfolder')
context_path = config.get('labkey_context_path', 'labkey')
schema = config.get('labkey_schema', 'core')
table = config.get('labkey_table', 'Users')

# Initialize APIWrapper with SSL and CSRF settings from configuration
api = APIWrapper(domain=labkey_server,
                 container_path=project_name,
                 context_path=context_path,
                 use_ssl=config.get('labkey_use_ssl', True),
                 verify_ssl=config.get('labkey_verify_ssl', True),
                 api_key=config.get('labkey_api_key'),
                 disable_csrf=config.get('labkey_disable_csrf', False))

def query_users():
    """Example function to query users from LabKey."""
    try:
        result = api.query.select_rows(schema, table)
        if result and 'rows' in result:
            print("select_rows: Number of rows returned:", str(result['rowCount']))
            for row in result['rows']:
                print(row)
        else:
            print(f'select_rows: Failed to load results from {schema}.{table}')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    query_users()
