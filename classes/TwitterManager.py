# twitter_manager.py
import os
import requests
from requests_oauthlib import OAuth1

# =======================================================
# Tweet class
class Tweet:

    def __init__(self, text, media_url, media_mime):
        self.contentStr     = text
        self.mediaUrl       = media_url
        self.mediaExt       = None
        if (mediaMine == "image/png"):
            self.mediaExt   = "png"
        elif (mediaMine == "image/gif"):
            self.mediaExt   = "gif"

    def send(self, auth):

        # step 0, download the media
        media_id == None
        if (self.mediaUrl and self.mediaExt):
            resp = requests.get(self.mediaUrl)
            resp.raise_for_status()
            with open(f"/tmp/rpgpowerforge_trello_media.{self.mediaExt}", "wb") as f:
                f.write(resp.content)

            # step 1 : upload media
            url = "https://upload.twitter.com/1.1/media/upload.json"

            response = None
            with open(f"/tmp/rpgpowerforge_trello_media.{self.mediaExt}", "rb") as file:
                print(self.mediaUrl)
                print(file)
                response = requests.post(url, auth=auth, files={"media": file})
                print(response.content)

            media_id = None
            if response:
                if "media_id" in response.json():
                    media_id = response.json()["media_id"]

            #safe exit
            if media_id == None:
                print("fail to upload media")
                return
            payload = {
            "text": self.contentStr,
            "media": {"media_ids": [str(media_id)]}
            }
        else:
            payload = {
                "text": self.contentStr
            }
        
        # step 2 post the tweet
        tweet_url = "https://api.twitter.com/2/tweets"

        return requests.post(tweet_url, auth=auth, json=payload)



class TwitterManager:
    """Manages Twitter API interactions."""
    
    def __init__(self, api_key, api_secret, access_token, 
                 access_token_secret, bearer_token):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.bearer_token = bearer_token
        print(self.api_key)
        print(self.api_secret)
        print(self.access_token)
        print(self.access_token_secret)
        self.client = None
        self._connect()
    
    def _connect(self):
        """Initialize connection to Twitter API."""
        try:
            self.client = OAuth1(
                self.api_key,
                self.api_secret,
                self.access_token,
                self.access_token_secret
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Twitter: {e}")
    
    def post_tweet(self, text, media_url, media_mime):
        """
        Post a tweet to Twitter.
        
        Args:
            text: The tweet text (max 280 characters)
            
        Returns:
            tuple: (success: bool, tweet_id: str or None)
        """        
        try:
            twt = Tweet(text, media_url, media_mime)
            response = twt.send(self.client)
            return True, None
        except Exception as e:
            print(f"✗ Unexpected error posting tweet: {e}")
            return False, None