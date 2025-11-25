# card_tracker.py
import json
import os
from pathlib import Path

class CardTracker:
    """Tracks which cards have been processed to avoid duplicates."""
    
    def __init__(self, storage_file='data/tracked_cards.json'):
        self.storage_file = storage_file
        self.tracked_cards = self._load()
    
    def _load(self):
        """Load tracked card IDs from storage file."""
        if not os.path.exists(self.storage_file):
            return set()
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                return set(data)
        except (json.JSONDecodeError, TypeError):
            print(f"Warning: Could not load {self.storage_file}, starting fresh")
            return set()
    
    def save(self):
        """Save tracked card IDs to storage file."""
        try:
            # first create it if the file does not exists
            file_path = Path(self.storage_file)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch(exist_ok=True)
            # save data in file
            with open(self.storage_file, 'w') as f:
                json.dump(list(self.tracked_cards), f, indent=2)
        except Exception as e:
            print(f"Error saving tracked cards: {e}")
    
    def is_tracked(self, card_id):
        """Check if a card ID is already tracked."""
        return card_id in self.tracked_cards
    
    def add(self, card_id):
        """Add a card ID to tracking."""
        self.tracked_cards.add(card_id)
        self.save()
    
    def remove(self, card_id):
        """Remove a card ID from tracking."""
        if card_id in self.tracked_cards:
            self.tracked_cards.discard(card_id)
            self.save()
    
    def clear(self):
        """Clear all tracked cards."""
        self.tracked_cards.clear()
        self.save()
    
    def get_new_cards(self, current_cards):
        """
        Compare current cards against tracked cards.
        
        Args:
            current_cards: List of card objects
            
        Returns:
            list: Cards that haven't been tracked yet
        """
        new_cards = []
        for card in current_cards:
            if not self.is_tracked(card.id):
                new_cards.append(card)
        return new_cards
    
    def count(self):
        """Return the number of tracked cards."""
        return len(self.tracked_cards)