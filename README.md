# 🛒 Django E-Commerce Platform (Jumia-Style)

A responsive Django-based e-commerce web app with full support for product categories, carts, search, wishlist, and a beautiful admin interface using Jazzmin.

## 🚀 Features

- 🔍 Search and filter by parent category
- 🧭 Breadcrumb navigation
- 🗂 Hierarchical categories (e.g., Men > T-Shirts)
- 🛒 Cart with quantity management and stock validation
- 🖼 Product image uploads with fallback
- ❤️ Wishlist system
- 🔐 Login-based cart and wishlist
- 🛠 Admin dashboard using **Jazzmin**

## 💾 Tech Stack

- **Bzackend:** Django, SQLite/PostgreSQL
- **Frontend:** Bootstrap 5, HTML, CSS, JS
- **Admin UI:** Jazzmin
- **Image Processing:** Pillow

## 📦 Installation

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📜 Requirements

Include the following in your `requirements.txt`:

```
Django>=4.0
Pillow
django-jazzmin
```

And add `jazzmin` to `INSTALLED_APPS` before `'django.contrib.admin'`:

```python
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    ...
]
```

## 🧑‍💻 Team

- **David Ibitokun** — Developer  
- **ChatGPT** — Documentation & Dev Support

## 📸 Screenshots

_Add screenshots of the home page, product card, cart page, and admin dashboard here._

## 📝 License

MIT License
