# main.py
from classes.TrelloTwitterBot import TrelloTwitterBot
import os

if __name__ == "__main__":

    # Configure the bot
    bot = TrelloTwitterBot()
    
    # run once
    # fetch trello + tweet if a new card is done
    bot.run_once()