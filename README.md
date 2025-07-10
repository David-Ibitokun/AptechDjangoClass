# 🛒 Django Product Management App

This is a Django-based web application for managing products. Users can create, list, and view detailed information about products, including images, pricing, availability, and more. Each product is associated with a user (creator), and slugs are automatically generated for SEO-friendly URLs.

---

## 📌 Features

- User-authenticated product creation
- Automatically generated, unique slugs for each product
- Product list view with grid layout
- Product detail view with full information
- Support for discount prices and stock quantities
- Admin interface with product listings

---

## 🧰 Tech Stack

- **Backend:** Django
- **Frontend:** HTML5, Bootstrap
- **Database:** SQLite (default, can be changed)
- **Image Uploads:** Django `ImageField`

---

## 🗂️ Project Structure

```

product\_app/
├── manage.py
├── products/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── templates/
│   │   └── products/
│   │       ├── product\_list.html
│   │       └── product\_detail.html
│   ├── urls.py
│   └── views.py
├── static/
│   └── images/
├── media/
│   └── products/
└── templates/
└── base.html

````

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/product-app.git
cd product-app
````

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> Example `requirements.txt`:

```txt
Django>=4.0,<5.0
Pillow
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (Optional for Admin)

```bash
python manage.py createsuperuser
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Now visit `http://127.0.0.1:8000/` in your browser.

---

## 🧾 Models

```python
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Slug is auto-generated using `slugify(name)` with uniqueness ensured.

---

## ✍️ Forms

```python
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['slug', 'creator']
```

---

## 🌐 Views

* **Add Product View**
* **Product List View**
* **Product Detail View**

Each view uses Django's templating system with Bootstrap UI.

---

## 🛠️ Admin Configuration

```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_available', 'creator', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
```

---

## 🖼️ Static & Media Files

* Images are uploaded to `/media/products/`
* Make sure `MEDIA_URL` and `MEDIA_ROOT` are configured:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

In `urls.py` (project level):

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🔒 Authenticated Product Creation

* Product creation is protected by login.
* You can use Django’s `@login_required` decorator or CBV mixins.

---

## 📸 Screenshots

*You can add screenshots here of:*

* Product list
* Product form
* Product detail page
* Admin panel

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add feature"`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙋‍♂️ Author

**Oliyide Adeoluwa John**
Founder @ Jexcel Technology
Email: [admin@jexceltech.com](mailto:admin@jexceltech.com)

