# twitter_manager.py
import tweepy

class TwitterManager:
    """Manages Twitter API interactions."""
    
    def __init__(self, api_key, api_secret, access_token, 
                 access_token_secret, bearer_token):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.bearer_token = bearer_token
        self.client = None
        #self._connect()
    
    def _connect(self):
        """Initialize connection to Twitter API."""
        try:
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
            # Test connection
            self.client.get_me()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Twitter: {e}")
    
    def post_tweet(self, text, media_url):
        """
        Post a tweet to Twitter.
        
        Args:
            text: The tweet text (max 280 characters)
            
        Returns:
            tuple: (success: bool, tweet_id: str or None)
        """        
        try:
            response = self.client.create_tweet(text=text)
            tweet_id = response.data['id']
            print(f"✓ Tweet posted successfully (ID: {tweet_id})")
            return True, tweet_id
        except tweepy.errors.TweepyException as e:
            print(f"✗ Twitter API error: {e}")
            return False, None
        except Exception as e:
            print(f"✗ Unexpected error posting tweet: {e}")
            return False, None