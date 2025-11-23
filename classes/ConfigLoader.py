# config_loader.py
import os
class ConfigLoader:
    """Handles loading and validation of configuration files."""
    
    def __init__(self):
        self.config = {
            "trello": {
                "api_key": os.getenv("TRELLO_API_KEY", "undefined"),
                "token": os.getenv("TRELLO_API_TOKEN", "undefined"),
                "board_id": "63d3c963ca6e394db2eb529f",
                "target_list_name": "Features Completed ✨"
            },
            "twitter": {
                "api_key": os.getenv("TWITTER_API_KEY", "undefined"),
                "api_secret": os.getenv("TWITTER_API_SECRET", "undefined"),
                "access_token": os.getenv("TWITTER_ACCESS_TOKEN", "undefined"),
                "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "undefined"),
                "bearer_token": os.getenv("TWITTER_BEARER_TOKEN", "undefined")
            }
        }
    
    def get_trello_config(self):
        return self.config["trello"]

    def get_twitter_config(self):
        return self.config["twitter"]
        
