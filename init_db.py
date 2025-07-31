import sqlite3
import bcrypt

def init_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    # Kullanıcı tablosu: role sütunu ekli ('admin' veya 'user')
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    )
    ''')

    # Ürün tablosu: user_id admin id olacak
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        stock INTEGER NOT NULL,
        price REAL NOT NULL,
        threshold INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # İlk admin kullanıcısını oluştur
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        username = 'admin'
        password = 'admin123'
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password_hash, 'admin'))
        print("[DB INIT] İlk admin kullanıcısı oluşturuldu (admin/admin123).")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
