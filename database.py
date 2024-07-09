# database.py
import sqlite3

def connect_db():
    conn = sqlite3.connect('bot.db')
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        telegram_id INTEGER UNIQUE,
                        username TEXT,
                        profile TEXT,
                        is_admin BOOLEAN DEFAULT 0
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                        id INTEGER PRIMARY KEY,
                        question TEXT
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS accesses (
                        id INTEGER PRIMARY KEY,
                        access_name TEXT,
                        description TEXT
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_access (
                        user_id INTEGER,
                        access_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (access_id) REFERENCES accesses (id)
                      )''')

    conn.commit()
    conn.close()

def initialize_commands(commands):
    conn = connect_db()
    cursor = conn.cursor()
    for command in commands:
        cursor.execute('INSERT OR IGNORE INTO accesses (access_name, description) VALUES (?, ?)', command)
    conn.commit()
    conn.close()

def add_user(telegram_id, username, profile):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (telegram_id, username, profile) VALUES (?, ?, ?)',
                   (telegram_id, username, profile))
    conn.commit()
    conn.close()

def get_user(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def get_admins():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE is_admin = 1')
    admins = cursor.fetchall()
    conn.close()
    return admins

def add_question(question):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO questions (question) VALUES (?)', (question,))
    conn.commit()
    conn.close()

def get_questions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions')
    questions = cursor.fetchall()
    conn.close()
    return questions

def get_questions_list():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions')
    questions = cursor.fetchall()
    conn.close()
    return questions

def add_access(access_name, description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO accesses (access_name, description) VALUES (?, ?)', (access_name, description))
    conn.commit()
    conn.close()

def get_accesses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accesses')
    accesses = cursor.fetchall()
    conn.close()
    return accesses

def get_access_list():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accesses')
    accesses = cursor.fetchall()
    conn.close()
    return accesses

def add_user_access(user_id, access_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_access (user_id, access_id) VALUES (?, ?)', (user_id, access_id))
    conn.commit()
    conn.close()

def remove_user_access(user_id, access_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_access WHERE user_id = ? AND access_id = ?', (user_id, access_id))
    conn.commit()
    conn.close()

def get_user_accesses(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT access_name FROM accesses INNER JOIN user_access ON accesses.id = user_access.access_id WHERE user_access.user_id = ?', (user_id,))
    accesses = cursor.fetchall()
    conn.close()
    return accesses

def set_admin(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_admin = 1 WHERE telegram_id = ?', (user_id,))
    conn.commit()
    conn.close()


def add_command(command_name, description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO accesses (access_name, description) VALUES (?, ?)', (command_name, description))
    conn.commit()
    conn.close()