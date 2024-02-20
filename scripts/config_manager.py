import os
import json


class ConfigManager:
    def __init__(self, default_config_path='config.json'):
        self.config = {}
        self.load_default_config(default_config_path)
        self.override_with_env_variables()

    def load_default_config(self, path):
        try:
            with open(path, 'r') as config_file:
                self.config = json.load(config_file)
                print(f"Loaded configuration: {self.config}")  # Debugging line
        except FileNotFoundError:
            print(f"Warning: Default configuration file {path} not found.")

    def override_with_env_variables(self):
        for key, value in os.environ.items():
            if key.startswith('APP_'):
                config_key = key[4:]  # Remove 'APP_' prefix
                self.config[config_key] = value
                # Debugging line
                print(f"Overriding {config_key} with environment variable.")

    def get(self, key, default=None):
        return self.config.get(key, default)
