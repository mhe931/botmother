import sqlite3

def connect_db():
    return sqlite3.connect('bot.db')

def execute_query(query, params=(), fetchone=False, fetchall=False):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone() if fetchone else cursor.fetchall() if fetchall else None
    conn.commit()
    conn.close()
    return result

def create_tables():
    execute_query('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        telegram_id INTEGER UNIQUE,
                        username TEXT,
                        profile TEXT,
                        is_admin BOOLEAN DEFAULT 0)''')
    execute_query('''CREATE TABLE IF NOT EXISTS questions (
                        id INTEGER PRIMARY KEY,
                        question TEXT)''')
    execute_query('''CREATE TABLE IF NOT EXISTS accesses (
                        id INTEGER PRIMARY KEY,
                        access_name TEXT,
                        description TEXT)''')
    execute_query('''CREATE TABLE IF NOT EXISTS user_access (
                        user_id INTEGER,
                        access_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (access_id) REFERENCES accesses (id))''')
    execute_query('''CREATE TABLE IF NOT EXISTS access_requests (
                        user_id INTEGER,
                        command_name TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id))''')

def initialize_commands(commands):
    for command in commands:
        execute_query('INSERT OR IGNORE INTO accesses (access_name, description) VALUES (?, ?)', command)

def add_user(telegram_id, username, profile):
    execute_query('INSERT INTO users (telegram_id, username, profile) VALUES (?, ?, ?)', (telegram_id, username, profile))

def get_user(telegram_id):
    return execute_query('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,), fetchone=True)

def get_admin(user_id):
    return execute_query('SELECT * FROM users WHERE telegram_id = ? AND is_admin = 1', (user_id,), fetchone=True)

def get_questions():
    return execute_query('SELECT * FROM questions', fetchall=True)

def add_question(question):
    execute_query('INSERT INTO questions (question) VALUES (?)', (question,))

def get_all_commands():
    return execute_query('SELECT access_name FROM accesses', fetchall=True)

def get_user_accesses(user_id):
    return execute_query('SELECT access_name FROM accesses INNER JOIN user_access ON accesses.id = user_access.access_id WHERE user_access.user_id = ?', (user_id,), fetchall=True)

def set_admin(user_id):
    execute_query('UPDATE users SET is_admin = 1 WHERE telegram_id = ?', (user_id,))

def add_access_request(user_id, command_name):
    execute_query('INSERT INTO access_requests (user_id, command_name) VALUES (?, ?)', (user_id, command_name))

def get_access_requests():
    return execute_query('SELECT * FROM access_requests', fetchall=True)

def delete_access_request(user_id, command_name):
    execute_query('DELETE FROM access_requests WHERE user_id = ? AND command_name = ?', (user_id, command_name))

def add_user_access(user_id, access_id):
    execute_query('INSERT INTO user_access (user_id, access_id) VALUES (?, ?)', (user_id, access_id))

def remove_user_access(user_id, access_id):
    execute_query('DELETE FROM user_access WHERE user_id = ? AND access_id = ?', (user_id, access_id))
