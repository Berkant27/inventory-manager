from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'stoktakipsistemi-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id_, username, password_hash, role):
        self.id = id_
        self.username = username
        self.password_hash = password_hash
        self.role = role

    @staticmethod
    def get(user_id):
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute("SELECT id, username, password, role FROM users WHERE id = ?", (user_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None

    @staticmethod
    def find_by_username(username):
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
@login_required
def index():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    if current_user.role == 'admin':
        # Admin tüm ürünleri görür
        c.execute("SELECT * FROM products")
    else:
        # Normal kullanıcılar sadece adminin ürünlerini görür
        admin_id = 1  # Varsayılan admin ID
        c.execute("SELECT * FROM products WHERE user_id = ?", (admin_id,))

    products = c.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.role != 'admin':
        flash('⚠️ Ürün ekleme yetkiniz yok.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        stock = int(request.form['stock'])
        price = float(request.form['price'])
        threshold = int(request.form['threshold'])

        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute(
            "INSERT INTO products (name, category, stock, price, threshold, user_id) VALUES (?, ?, ?, ?, ?, ?)",
            (name, category, stock, price, threshold, current_user.id)
        )
        conn.commit()
        conn.close()
        flash('✅ Ürün başarıyla eklendi.', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.role != 'admin':
        flash('⚠️ Ürün düzenleme yetkiniz yok.', 'danger')
        return redirect(url_for('index'))

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id = ?", (id,))
    product = c.fetchone()
    if not product:
        flash('❌ Ürün bulunamadı.', 'danger')
        conn.close()
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        stock = int(request.form['stock'])
        price = float(request.form['price'])
        threshold = int(request.form['threshold'])

        c.execute("""
            UPDATE products SET name=?, category=?, stock=?, price=?, threshold=?
            WHERE id=?
        """, (name, category, stock, price, threshold, id))
        conn.commit()
        conn.close()
        flash('✅ Ürün başarıyla güncellendi.', 'success')
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', product=product)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    if current_user.role != 'admin':
        flash('⚠️ Ürün silme yetkiniz yok.', 'danger')
        return redirect(url_for('index'))

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('✅ Ürün başarıyla silindi.', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'login':
            username = request.form['username']
            password = request.form['password']
            user = User.find_by_username(username)
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
                login_user(user)
                flash('✅ Giriş başarılı.', 'success')
                return redirect(url_for('index'))
            else:
                flash('❌ Kullanıcı adı veya şifre hatalı.', 'danger')
                return redirect(url_for('login'))

        elif action == 'register':
            username = request.form['reg_username']
            password = request.form['reg_password']
            password_confirm = request.form['reg_password_confirm']

            if password != password_confirm:
                flash('❌ Şifreler uyuşmuyor.', 'danger')
                return redirect(url_for('login'))

            if User.find_by_username(username):
                flash('❌ Bu kullanıcı adı zaten alınmış.', 'danger')
                return redirect(url_for('login'))

            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            conn = sqlite3.connect('db.sqlite3')
            c = conn.cursor()
            # Yeni kullanıcı her zaman 'user' rolü ile kaydedilir
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password_hash, 'user'))
            conn.commit()
            conn.close()

            flash('✅ Kayıt başarılı, şimdi giriş yapabilirsiniz.', 'success')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('✅ Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
