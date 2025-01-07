from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor


def get_user_by_username(mysql, username):
    """Retrieve a user by their username"""
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    return cursor.fetchone()


def insert_user(mysql, username, password_hash):
    """Insert a new user into the database"""
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password_hash))
    mysql.connection.commit()


def update_user_password(mysql, email, hashed_password):
    """Update the password for a user in the database"""
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE users SET password = %s WHERE username = %s', (hashed_password, email))
    mysql.connection.commit()
