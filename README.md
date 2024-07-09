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


### User Access Journey
## User Starts Interaction:

1. The user sends the /start command to the bot.
* The bot checks if the user is already registered.
* User Registration:

2. If the user is not registered, the bot asks a series of questions (retrieved from the database).
* The user answers these questions one by one.
* Once all questions are answered, the user's profile is created and stored in the database.
* The bot notifies the admin about the new user registration.

3. Admin Reviews User Profile:

* The admin receives a message from the bot with the new user's profile details.
* The admin decides whether to grant access to the user.

4. User Access:

* The user can send the /help command to see the list of available commands they can use.
* The commands available to the user are determined by the access permissions granted by the admin.

## Admin Access Journey
1. Admin Starts Interaction:

* The admin sends the /start command to the bot.
* The bot checks if the admin is already registered. If not, the admin follows the same registration process as a regular user.
2. Admin Manages Access Permissions:

* The admin can view and manage user access permissions using the /accesslist command.
* The bot displays a list of users along with the commands they can access.
* Each user in the list has an inline keyboard button to modify their access permissions.
3. Admin Modifies Access Permissions:

* When the admin clicks on a user's inline button, the bot shows the list of all possible accesses for that user.
* The admin can grant or revoke specific access permissions using the inline keyboard buttons.
4. Admin Adds New Access Entries:

* The admin can add new access entries using the /addaccess command.
* The bot starts a conversation, prompting the admin to enter the access name and description.
* The new access entry is added to the database and can be granted to users.
5. Admin Commands Overview:

/userlist: View a list of all users.
/adminlist: View a list of all admins.
/accesslist: View and manage access permissions for users.
/nameparamlist: View and manage profile questions.
/addaccess: Start the process to add a new access entry.
/setadmin <user_id>: Grant admin rights to a user.
## Detailed Code Walkthrough for Admin Access Management
Here’s how the admin can manage user access permissions using the bot:

1. View Access List:

* The admin sends the /accesslist command.
* The bot retrieves the list of all users and their current access permissions.
* The bot sends a message with an inline keyboard, allowing the admin to select a user to modify their accesses.
2. Modify User Access:

* The admin clicks on a user's button in the access list.
* The bot displays the list of all possible accesses for that user, with buttons to grant or revoke each access.
* The admin clicks the "Grant" or "Revoke" button to modify the user's access permissions.
* The bot updates the database and confirms the change.
Here’s a simplified flow:

```vbnet
admin: /accesslistBot: [Displays list of users with their accesses]Admin: Clicks on a user's inline buttonBot: [Displays list of accesses for the selected user with Grant/Revoke buttons]Admin: Clicks "Grant Access X"Bot: Access X granted to user Y
```

## Implementation Details in handlers.py
The relevant functions in handlers.py for this journey include:

help_command: Shows available commands to the user based on their access permissions.
accesslist: Displays a list of users and their accesses.
button: Handles the inline button clicks to show/grant/revoke accesses.
grant_access: Grants a specific access to a user.
revoke_access: Revokes a specific access from a user.
