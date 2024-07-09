# bot.py
import database as db
import handlers

if __name__ == '__main__':
    db.create_tables()
    handlers.main()



    """
    ## Running the Bot
        Ensure config.py is correctly configured with your bot token and admin ID.
        Run bot.py to start the bot.
    
        ```bash
        python bot.py
        ```

    """ 