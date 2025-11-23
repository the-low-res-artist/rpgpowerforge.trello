# bot.py
import time
import json
from datetime import datetime
from classes.ConfigLoader import ConfigLoader
from classes.TrelloManager import TrelloManager
from classes.TwitterManager import TwitterManager
from classes.CardTracker import CardTracker

class TrelloTwitterBot:
    """Main bot orchestrator that coordinates all components."""
    
    def __init__(self):
        print("Initializing Trello to Twitter Bot...")
        
        # Load configuration
        self.config = ConfigLoader()
        
        # Initialize managers
        self._init_trello()
        self._init_twitter()
        
        # Initialize card tracker
        self.tracker = CardTracker()
        
        print(f"Bot initialized successfully:")
        print(f" - Board: {self.trello.get_board_name()}")
        print(f" - Watching list: '{self.trello.get_list_name()}'")
        print(f" - Cards tracked: {self.tracker.count()}")
    
    def _init_trello(self):
        """Initialize Trello manager."""
        trello_config = self.config.get_trello_config()
        self.trello = TrelloManager(
            api_key=trello_config['api_key'],
            token=trello_config['token'],
            board_id=trello_config['board_id'],
            target_list_name=trello_config['target_list_name']
        )
    
    def _init_twitter(self):
        """Initialize Twitter manager."""
        twitter_config = self.config.get_twitter_config()
        self.twitter = TwitterManager(
            api_key=twitter_config['api_key'],
            api_secret=twitter_config['api_secret'],
            access_token=twitter_config['access_token'],
            access_token_secret=twitter_config['access_token_secret'],
            bearer_token=twitter_config['bearer_token']
        )
    
    def check_and_tweet(self):
        """Check for new cards and tweet about them."""
        # Get current cards in target list
        current_cards = self.trello.get_cards_in_target_list()
        
        # safely skip the first card (pinned card)
        current_cards = current_cards[1:]

        # Find new cards
        new_cards = self.tracker.get_new_cards(current_cards)
        
        if not new_cards:
            return 0
        
        print(f"Found {len(new_cards)} new card(s):")
        tweeted_count = 0
        
        for card in new_cards:
            print(f"\nNew card : {card.name}")
            
            # skip if it's the version card (should already skipped because pinned but we double-check)
            if (card.name.startswith("version")):
              continue
            
            # get the cover url
            card.fetch(eager=True) 

            # Access the cover from the card's client
            cover_attachment_id = None
            card_data = card.client.fetch_json(f'/cards/{card.id}', http_method='GET')
            if ("cover" in card_data and "idAttachment" in card_data["cover"]):
                cover_attachment_id = card_data["cover"]["idAttachment"]

            # get the cover url from the attachments
            cover_attachment_url = None
            for attachment in card.attachments:
                if (attachment['mimeType'] in "image/gif image/png" and "url" in attachment and cover_attachment_id == attachment["id"]):
                    cover_url = attachment["url"]

            # get card labels
            labels_list = []
            for label in card.labels:
                labels_list.append(self.format_label(label))
            labels = " ".join(labels_list)
           
            # Format tweet
            intro = "🤖 *bip boop* Progress report !\n\nNew feature done : "
            tweet_text = intro + card.name
            if (labels != ""):
                tweet_text += "\n\n" + labels

            # Post tweet
            success, tweet_id = self.twitter.post_tweet(tweet_text, cover_url)
            
            if success:
                # Mark card as tracked
                self.tracker.add(card.id)
                tweeted_count += 1
            else:
                print(f"Skipping card tracking due to tweet failure")
        
        return tweeted_count
    
    def format_label(self, label):
        emoji = "⚫"
        emojis = {
            "blue":   "🔵",
            "sky":    "🔵",
            "green":  "🟢",
            "lime":   "🟢",
            "yellow": "🟡",
            "orange": "🟠",
            "red":    "🔴",
            "purple": "🟣",
            "pink":   "🟣",
            "black":  "⚫"
        }
        for key, val in emojis.items():
            if (key in label.color):
                emoji = val
                break
        
        return f"[{emoji} {label.name}]"

    def run_once(self):
        """Run one check cycle."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n[{timestamp}] Checking for new cards...")
        
        try:
            tweeted_count = self.check_and_tweet()
            if tweeted_count == 0:
                print("No new cards found")
            else:
                print(f"\n✓ Posted {tweeted_count} tweet(s)")
        except Exception as e:
            print(f"Error during check: {e}")
            raise