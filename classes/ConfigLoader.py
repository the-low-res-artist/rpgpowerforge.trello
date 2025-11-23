# config_loader.py
import json

class ConfigLoader:
    """Handles loading and validation of configuration files."""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load()
    
    def load(self):
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            self._validate(config)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Config file '{self.config_file}' not found. "
                "Please create it based on config.json.example"
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
    
    def _validate(self, config):
        """Validate that all required configuration keys exist."""
        required_keys = {
            'trello': ['api_key', 'token', 'board_id', 'target_list_name'],
            'twitter': ['api_key', 'api_secret', 'access_token', 
                       'access_token_secret', 'bearer_token']
        }
        
        for section, keys in required_keys.items():
            if section not in config:
                raise ValueError(f"Missing '{section}' section in config")
            for key in keys:
                if key not in config[section]:
                    raise ValueError(
                        f"Missing '{key}' in '{section}' section of config"
                    )
    
    def get_trello_config(self):
        """Get Trello-specific configuration."""
        return self.config['trello']
    
    def get_twitter_config(self):
        """Get Twitter-specific configuration."""
        return self.config['twitter']
    
    def get_tweet_template(self):
        """Get tweet template with default fallback."""
        return self.config.get(
            'tweet_template', 
            'New update: {card_name} 🎯\n{card_url}'
        )
    
    def get_check_interval(self):
        """Get check interval in seconds with default fallback."""
        return self.config.get('check_interval_seconds', 300)