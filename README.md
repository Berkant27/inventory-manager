# 📦 Inventory Manager – Akıllı Stok Takip Sistemi

Bu proje, küçük ve orta ölçekli işletmelerin ürün stoklarını takip edebilmesi için geliştirilmiş web tabanlı bir stok yönetim sistemidir. Flask ve SQLite teknolojileri kullanılarak oluşturulmuştur.

---

## 🚀 Özellikler

- 🔐 *Kullanıcı Girişi / Kayıt Sistemi*  
- 👤 *Rol Bazlı Erişim (Admin / Kullanıcı)*  
- ➕ *Ürün Ekleme, Güncelleme, Silme (sadece admin)*  
- 📊 *Kritik stok seviyesi uyarıları*  
- 🔍 *Kategoriye göre filtreleme ve arama (geliştirilebilir)*  
- 📄 *PDF/CSV raporlama ve grafik desteği (opsiyonel modül)*

---

## 🛠 Teknolojiler

| Teknoloji      | Açıklama                           |
|----------------|------------------------------------|
| Python         | Uygulama dili                      |
| Flask          | Web framework                      |
| Flask-Login    | Kimlik doğrulama sistemi           |
| SQLite         | Hafif veritabanı                   |
| Bootstrap 5    | Modern ve responsive arayüz        |
| bcrypt         | Güvenli şifreleme                  |

---

## 📂 Kurulum

```bash
# Gerekli kütüphaneleri yükle
pip install -r requirements.txt

# Veritabanını oluştur
python init_db.py

# Uygulamayı başlat
python app.py

📝 Uygulama ilk çalıştığında, ilk kayıt olan kullanıcı otomatik olarak admin olarak atanır.


---

🔐 Kullanıcı Rolleri

Rol	Yetkiler

Admin	Ürün ekleme, düzenleme, silme
User	Ürünleri yalnızca görüntüleme



---

📁 Klasör Yapısı

inventory-manager/
├── app.py
├── init_db.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── add.html
│   ├── edit.html
│   └── login.html
├── static/
│   └── style.css
├── db.sqlite3         # (otomatik oluşur)
└── .gitignore


---

📌 Notlar

Sistem geliştirilebilir mimaride yazılmıştır.

Yeni özellikler (stok analizi, çoklu depo, API entegrasyonu vs.) kolayca eklenebilir.

Eğer sistem canlıya alınacaksa, Flask’ın production ayarları yapılmalıdır (örneğin: Gunicorn + Nginx).



---

📬 Katkı / Geri Bildirim

Pull request ve önerilere açıktır.
Her türlü katkı, hata bildirimi ya da geliştirme önerisi için lütfen iletişime geçin.


---

