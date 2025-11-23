# main.py
from classes.TrelloTwitterBot import TrelloTwitterBot
import os

if __name__ == "__main__":

    # Configure the bot
    bot = TrelloTwitterBot('config/config.json')
    
    # run once
    # fetch trello + tweet is a new card is done
    bot.run_once()