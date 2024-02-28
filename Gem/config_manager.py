import os
import json
import logging

class ConfigManager:
    def __init__(self, default_config_path='config.json'):
        self.config_path = default_config_path
        self.config = self.load_default_config()

    def load_default_config(self):
        """Loads the default configuration from a JSON file."""
        try:
            with open(self.config_path, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            logging.warning(f"Default configuration file {self.config_path} not found. Using defaults.")
            return {}
    
    def save_config(self):
        """Saves the current configuration back to the file."""
        try:
            with open(self.config_path, 'w') as config_file:
                json.dump(self.config, config_file, indent=4)
            logging.info("Configuration saved successfully.")
        except Exception as e:
            logging.error(f"Failed to save configuration: {e}")

    def get(self, key, default=None):
        """Retrieves a configuration value for a given key or returns a default if not found."""
        return self.config.get(key, default)



############################

import os
import json
import logging

class ConfigManager:
    def __init__(self, default_config_path='config.json'):
        self.config = {}
        self.load_default_config(default_config_path)
    
    def load_default_config(self, path):
        """Loads the default configuration from a JSON file."""
        try:
            with open(path, 'r') as config_file:
                self.config = json.load(config_file)
                logging.info(f"Loaded configuration from {path}")
        except FileNotFoundError:
            logging.warning(f"Default configuration file {path} not found. Using defaults.")

    def get(self, key, default=None):
        """Retrieves a configuration value for a given key or returns a default if not found."""
        return self.config.get(key, default)
