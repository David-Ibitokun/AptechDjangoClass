
# 🛒 Sumia E-Commerce Platform

Sumia is a modern, responsive Django-based e-commerce web application designed for seamless product browsing, vendor management, category navigation, tag suggestion, and secure checkout.

## 🚀 Features

- 🔐 User Authentication & Registration
- 🛍️ Product Browsing by Category & Tags
- 🏷️ Smart Tag Suggestions with Autocomplete (like hashtags)
- 🧑‍💻 Vendor Dashboard to Manage Products
- 📂 Hierarchical Categories with SVG Icons (e.g. Men > T-Shirts)
- 📦 Cart, Wishlist, and Orders Functionality
- 🧭 Breadcrumb Navigation
- 🔎 Search & Filter Products
- 📧 Email Notifications
- 📱 Mobile-Responsive Design
- 🎨 Admin UI Styled with Jazzmin
- 🖼️ Image Preview Before Upload
- 🗃️ Tag Management using `django-taggit` + `Select2`

## 🖼️ Homepage Preview

The homepage includes:

- Hero Banner
- Sidebar with Parent Categories (hover to view subcategories)
- Grid of Featured Products
- Interactive Tags (#summer, #fashion, etc.)
- Smooth Add to Cart / Wishlist interactions

## 🛠️ Technologies Used

- **Backend:** Django, Django ORM
- **Frontend:** HTML5, CSS3, Bootstrap 5, Select2
- **Admin Theme:** [Jazzmin](https://github.com/farridav/django-jazzmin)
- **Tagging:** django-taggit + select2.js
- **Icons:** SVG Icons for categories

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/David-Ibitokun/AptechDjangoClass
   cd sumia-ecommerce
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the server:
   ```bash
   python manage.py runserver
   ```

## 📂 Requirements

See the `requirements.txt` file, which includes:

- Django
- django-taggit
- django-select2
- django-jazzmin
- pillow

## 👨‍👩‍👧‍👦 Team Collaboration

This project was a team effort involving:

- **Backend Logic & Database Modeling**
- **Vendor Dashboard & Tagging System**
- **SVG Icon Management & UI Styling**
- **Category Navigation & Subcategory Hover UI**
- **Autocomplete API for Tags**
- **Documentation & Deployment Setup**

## 📑 Documentation

The full project documentation is available in `sumia_project_documentation.docx`.

---

🛍️ Happy Shopping with Sumia!
