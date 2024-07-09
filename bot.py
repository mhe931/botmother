import config
import database as db
from handlers import main

def initialize():
    db.create_tables()
    db.initialize_commands(config.AVAILABLE_COMMANDS)

if __name__ == '__main__':
    initialize()
    main()
 

    """
    ## Running the Bot
        Ensure config.py is correctly configured with your bot token and admin ID.
        Run bot.py to start the bot.
    
        ```bash
        python bot.py
        ```

    """ 