import sqlite3

# Veritabanı bağlantısını kurma
conn = sqlite3.connect('example.db')
c = conn.cursor()

# Kullanıcı tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, username TEXT, display_name TEXT, phone TEXT, email TEXT, user_role TEXT, enable BOOLEAN)''')
conn.commit()

def insert_user(username, display_name, phone, email, user_role, enable):
    c.execute("INSERT INTO users (username, display_name, phone, email, user_role, enable) VALUES (?, ?, ?, ?, ?, ?)",
              (username, display_name, phone, email, user_role, enable))
    conn.commit()

def fetch_users(show_disabled):
    if show_disabled:
        c.execute("SELECT * FROM users ORDER BY id")
    else:
        c.execute("SELECT * FROM users WHERE enable = 1 ORDER BY id")
    return c.fetchall()