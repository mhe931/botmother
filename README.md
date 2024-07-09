# Telegram User Management Bot

This is a Telegram bot built using the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library. The bot manages users, allowing an admin to approve user profiles and assign access permissions. User data is stored in an SQLite database with password protection.

## Features

- **User Registration:** Users can register by answering a series of questions.
- **Admin Approval:** User profiles are sent to an admin for approval.
- **Access Management:** Admins can assign, edit, or delete access permissions for users.
- **Command Forwarding:** All user commands are forwarded to a specified Telegram channel.
- **Admin Commands:**
  - `/userlist`: View a list of users.
  - `/adminlist`: View a list of admins.
  - `/accesslist`: View and manage access permissions.
  - `/nameparamlist`: View and manage profile questions.

## Requirements

- Python 3.6+
- `python-telegram-bot` library
- SQLite

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/mhe931/telegram-user-management-bot.git
    cd telegram-user-management-bot
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `config.py` file and add your bot token and admin ID:
    ```python
    # config.py
    BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
    ADMIN_ID = 123456789  # Replace with the actual admin ID
    ```

5. Initialize the database:
    ```bash
    python bot.py
    ```

## Running the Bot

1. Start the bot:
    ```bash
    python bot.py
    ```

## Project Structure

telegram-user-management-bot/
├── database.py # Database management
├── handlers.py # Bot command and message handlers
├── bot.py # Main bot entry point
├── config.py # Configuration file (git ignored)
├── requirements.txt # Python dependencies
└── README.md # Project documentation


## Database Structure

- **users**: Stores user profiles.
- **questions**: Stores registration questions.
- **accesses**: Stores access permissions.
- **user_access**: Maps users to their access permissions.

## Bot Commands

### User Commands

- `/start`: Begin the registration process.

### Admin Commands

- `/userlist`: View a list of users.
- `/adminlist`: View a list of admins.
- `/accesslist`: View and manage access permissions.
- `/nameparamlist`: View and manage profile questions.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/mhe931/botmother/blob/main/LICENSE) file for more details.
