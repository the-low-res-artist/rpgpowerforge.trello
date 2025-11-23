# trello_manager.py
from trello import TrelloClient

class TrelloManager:
    """Manages Trello API interactions."""
    
    def __init__(self, api_key, token, board_id, target_list_name):
        self.api_key = api_key
        self.token = token
        self.board_id = board_id
        self.target_list_name = target_list_name
        self.client = None
        self.board = None
        self.target_list = None
        self._connect()
    
    def _connect(self):
        """Initialize connection to Trello."""
        try:
            print(f"Initialize connection to Trello.")
            self.client = TrelloClient(
                api_key=self.api_key,
                token=self.token
            )
            print(f"Connection extablished, finding board...")
            self.board = self.client.get_board(self.board_id)
            print(f"Board found, finding list...")
            self.target_list = self._find_target_list()
            print(f"List found")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Trello: {e}")
    
    def _find_target_list(self):
        """Find and return the target list on the board."""
        lists = self.board.list_lists()
        for lst in lists:
            if lst.name == self.target_list_name:
                return lst
        
        available_lists = [lst.name for lst in lists]
        raise ValueError(
            f"List '{self.target_list_name}' not found on board. "
            f"Available lists: {', '.join(available_lists)}"
        )
    
    def get_cards_in_target_list(self):
        """Get all cards currently in the target list."""
        try:
            return self.target_list.list_cards()
        except Exception as e:
            print(f"Error fetching cards: {e}")
            # Reconnect and try again
            self._connect()
            return self.target_list.list_cards()
    
    def get_board_name(self):
        """Get the name of the board."""
        return self.board.name
    
    def get_list_name(self):
        """Get the name of the target list."""
        return self.target_list_name