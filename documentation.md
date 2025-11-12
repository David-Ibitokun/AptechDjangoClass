# Sumia E-Commerce Platform Documentation

## 1. Project Overview

Sumia is a comprehensive e-commerce platform built with Django. It provides a multi-vendor marketplace where users can register as either regular customers or vendors. Vendors can manage their own products, while customers can browse, search, purchase products, and manage their orders. The project is designed with a clear separation of concerns, utilizing Django apps for different functionalities and a rich data model to support a modern online shopping experience.

The existing `README.md` file mentions that this was a collaborative team effort, focusing on backend logic, vendor systems, UI/UX, and documentation.

### Key Features:
-   **Dual User Roles:** Separate account types for 'User' and 'Vendor'.
-   **Vendor Dashboard:** A dedicated dashboard for vendors to add, edit, delete, and view their products and orders.
-   **Customer Dashboard:** A dashboard for users to view their profile, order history, and manage account details.
-   **Product & Catalog Management:** Products are organized by hierarchical categories and brands.
-   **Hierarchical Categories:** Categories can have parents and children, allowing for structured navigation (e.g., Electronics > Laptops). Icons are automatically assigned to categories based on keywords.
-   **Shopping Cart & Wishlist:** Standard e-commerce features for users to save products for purchase.
-   **Order Management:** A complete order workflow from checkout to delivery, with separate views for customers and vendors.
-   **Advanced Search:** Users can search for products by name, description, category, brand, or tags.
-   **Custom Admin Interface:** The Django admin is styled using `django-jazzmin` for an improved user experience.

## 2. Technologies & Dependencies

The project is built on Python and the Django framework. The specific dependencies are listed in `requirements.txt`:

-   **`Django>=4.2,<5.0`**: The core web framework.
-   **`pillow>=10.0.0`**: For image handling (e.g., product images, brand logos).
-   **`django-jazzmin>=2.6.0`**: A drop-in theme for the Django admin site to make it more modern.
-   **`django-widget-tweaks>=1.4.12`**: Used to customize form field rendering in templates.
-   **`django-taggit>=3.1.0`**: Provides tagging functionality for products.
-   **`django-select2>=8.0`**: Integrates the Select2 JavaScript library for enhanced `<select>` elements, likely used for tags or category selection.

## 3. Installation & Setup

Based on the `README.md` and standard Django practices, here is how to set up the project locally:

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd Django_Class
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser** (for admin access):
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.

## 4. Project Structure

The project is organized into three main Django apps: `sumia`, `authentications`, and `pages`.

-   **`sumia/`**: This is the main project package.
    -   `settings.py`: Contains all project-level settings, including `INSTALLED_APPS`, `MIDDLEWARE`, database configuration, and settings for third-party packages like `JAZZMIN_SETTINGS`.
    -   `urls.py`: The root URLconf. It routes incoming requests to the `pages` and `authentications` apps.
    -   `wsgi.py` & `asgi.py`: Standard files for deploying the application.

-   **`authentications/`**: This app handles user management.
    -   `models.py`: Defines the custom user model `UsersRegistration`, which extends Django's `AbstractUser` to include an `account_type` field.
    -   `views.py`: Contains the logic for user registration, login, logout, and the user/vendor-specific dashboards.
    -   `urls.py`: Defines the URL patterns for this app, prefixed with `/auth/`.
    -   `forms.py`: Contains the `UsersRegistrationForm` for new user sign-ups.

-   **`pages/`**: This is the core e-commerce app.
    -   `models.py`: Defines the primary data models for the application: `Category`, `Brand`, `Product`, `Cart`, `CartItem`, `Wishlist`, `Order`, and `OrderItem`.
    -   `views.py`: Contains the majority of the application's logic, including views for the homepage, product details, category pages, cart management, checkout, and vendor/user order management.
    -   `urls.py`: Defines the extensive URL patterns for all public-facing pages and user actions.

## 5. Database Models

### `authentications.models.UsersRegistration`
This model extends Django's built-in `User` to support different account types.
-   `account_type`: A `CharField` with choices 'user' or 'vendor'. This is crucial for differentiating between customers and sellers.
-   `agreed_to_terms`: A `BooleanField` to confirm that the user has agreed to terms and conditions upon registration.

### `pages.models`
This app contains the core e-commerce models.

-   **`Category`**: Represents product categories.
    -   Fields: `name`, `slug`, `parent` (self-referencing for subcategories), `description`, `icon`.
    -   Logic: Automatically generates a unique `slug` and assigns a Font Awesome icon from a predefined map based on the category name.

-   **`Brand`**: Represents product brands.
    -   Fields: `name`, `slug`, `description`, `logo`.

-   **`Product`**: The central model for items sold on the platform.
    -   Fields: `name`, `slug`, `description`, `price`, `discount_price`, `image`, `stock_quantity`, `is_available`.
    -   Relationships: Linked to `Category`, `Brand`, and `creator` (a `User` who is a vendor). Also uses `TaggableManager` for tags.

-   **`Cart` & `CartItem`**: Manages the shopping cart functionality.
    -   `Cart`: Linked one-to-one with a `User`.
    -   `CartItem`: A through-model linking a `Cart` to a `Product` with a specified `quantity`.

-   **`Wishlist`**: Allows users to save products they are interested in. Linked to a `User` and a `Product`.

-   **`Order` & `OrderItem`**: Manages customer orders.
    -   `Order`: Contains customer information, shipping details (`address`, `city`, etc.), `total_price`, `status` (e.g., 'pending', 'shipped'), and a unique `order_number`.
    -   `OrderItem`: A through-model linking an `Order` to a `Product`, storing the `quantity` and the `price_at_purchase`.

## 6. URL Endpoints and Views

### Authentication (`/auth/...`)
-   `/auth/register/`: `register_user` view. Handles new user creation.
-   `/auth/login/`: `login_user` view. Authenticates users and redirects them based on their `account_type`.
-   `/auth/logout/`: `logout_user` view. Logs the user out.
-   `/auth/dashboard/user/`: `user_dashboard` view. Displays the customer dashboard.
-   `/auth/dashboard/vendor/`: `vendor_dashboard` view. Displays the vendor dashboard with a list of their products.
-   `/auth/myProfile/`: `myProfile` view. Allows users to view and update their profile information.

### Pages (Root URL `/`)
-   `/`: `home` view. The main landing page.
-   `/shop/`: `shop` view. Displays all available products.
-   `/about/` & `/contact/`: Static pages.
-   `/product/<slug>/`: `product_detail` view. Shows details for a single product.
-   `/category/<slug>/`: `category_detail` view. Lists all products within a category and its subcategories.
-   `/brands/` & `/brands/<slug>/`: `brand_list` and `brand_detail` views.

### Cart and Checkout
-   `/cart/`: `view_cart` view. Displays the contents of the user's shopping cart.
-   `/cart/add/<product_id>/`: `add_to_cart` view. Adds a product to the cart.
-   `/cart/remove/<item_id>/`: `remove_from_cart` view.
-   `/cart/update/<item_id>/`: `update_cart_quantity` view.
-   `/checkout/`: `checkout` view. Handles the order creation process.

### User and Vendor Actions
-   `/my-orders/`: `recent_order` view. Lists a user's past orders.
-   `/my-orders/<order_number>/`: `users_order_detail` view. Shows details of a specific order for a customer.
-   `/vendor/orders/`: `vendor_orders` view. Lists all orders containing products sold by the logged-in vendor.
-   `/vendor/orders/<order_number>/`: `vendor_order_detail` view. Shows order details for a vendor, filtered to their products only.
-   `/product/add/`, `/product/<slug>/edit/`, `/product/<slug>/delete/`: Views for vendors to manage their products.

## 7. Application Flow

### User (Customer) Flow

1.  **Registration:** A new user visits the `/auth/register/` page, fills out the registration form, selects the "user" account type, and agrees to the terms.
2.  **Login:** The user logs in via the `/auth/login/` page and is redirected to their dashboard at `/auth/dashboard/user/`.
3.  **Browsing:** The user can browse products on the home page (`/`), shop page (`/shop/`), or by visiting specific category or brand pages.
4.  **Adding to Cart:** On a product detail page, the user can add a product to their cart.
5.  **Checkout:** The user proceeds to checkout from the cart page (`/cart/`), fills in their shipping details, and places the order.
6.  **Order History:** The user can view their past orders on the `/my-orders/` page and see details for each order.

### Vendor Flow

1.  **Registration:** A new vendor registers via the `/auth/register/` page, selecting the "vendor" account type.
2.  **Login:** The vendor logs in and is redirected to their dashboard at `/auth/dashboard/vendor/`.
3.  **Product Management:** From their dashboard, a vendor can:
    *   Add a new product using the `/product/add/` page.
    *   Edit an existing product.
    *   Delete a product.
4.  **Order Management:** The vendor can view orders containing their products on the `/vendor/orders/` page. They can see the details of each order to manage fulfillment.

## 8. Frontend Structure

The frontend is built using standard Django templates, with CSS and JavaScript for styling and interactivity.

-   **`templates/`**: This directory at the project root contains all the HTML templates.
    -   **`base.html`**: This is the master template. It includes the main HTML structure, header, footer, and includes for static files (CSS/JS). All other templates extend this file.
    -   **Partials:** The header and footer are likely included in `base.html` or other templates to ensure consistency.
    -   **App-specific templates:** Templates are organized by their functionality (e.g., `product_detail.html`, `cart.html`, `login.html`).

-   **`authentications/static/`**: This directory contains the static assets for the project.
    -   **`css/`**: Contains the main stylesheet (`style.css`), a CSS reset (`normalize.css`), and vendor-specific CSS.
    -   **`js/`**: Contains JavaScript files for frontend interactivity.
    -   **`images/`**: Contains all the images used in the templates, such as logos, banners, and product icons.

-   **`django-widget-tweaks`**: This library is used to render form fields with custom HTML attributes (like CSS classes and placeholders) directly in the templates, making it easier to style forms without creating custom form widgets in Python. For example, you might see `{{ form.my_field|attr:"class:form-control" }}` in the templates.

## 9. Deployment

Deploying a Django project to a production environment requires a different setup than the local development server. Here are the key steps and considerations:

1.  **`settings.py` Configuration:**
    *   **`DEBUG`**: This **must** be set to `False` in production for security and performance reasons.
    *   **`SECRET_KEY`**: The secret key used in development is not secure enough for production. It should be replaced with a unique, randomly generated key, preferably loaded from an environment variable.
    *   **`ALLOWED_HOSTS`**: This list must be populated with the domain name(s) that will host the application (e.g., `['www.sumia.com']`).

2.  **Static Files:**
    *   Run `python manage.py collectstatic` to gather all static files from the project and its apps into a single directory (defined by `STATIC_ROOT` in `settings.py`).
    *   A web server like Nginx should be configured to serve these static files directly.

3.  **Web Server Gateway Interface (WSGI):**
    *   The development server (`manage.py runserver`) is not suitable for production.
    *   A production-grade WSGI server like **Gunicorn** or **uWSGI** should be used to run the application. For example, with Gunicorn:
        ```bash
        gunicorn sumia.wsgi:application
        ```

4.  **Database:**
    *   While SQLite (`db.sqlite3`) is convenient for development, a more robust database like **PostgreSQL** or **MySQL** is recommended for production.

5.  **Hosting:**
    *   The project can be deployed on various platforms, such as Heroku, AWS, DigitalOcean, or PythonAnywhere. Each platform has its own deployment process.

## 10. Testing

The project includes `tests.py` files within the `authentications` and `pages` apps, indicating that a testing structure is in place.

### Running Tests

To run the entire test suite, execute the following command:

```bash
python manage.py test
```

This command will discover and run all tests in the project.

### Testing Strategy

While the specific tests are not detailed here, a standard Django testing approach would include:

-   **Model Tests:** To ensure that the database models behave as expected (e.g., custom methods, relationships).
-   **View Tests:** To verify that views render the correct templates, handle form submissions correctly, and implement the expected logic. This is often done using Django's test client to simulate HTTP requests.
-   **Form Tests:** To check that forms are valid with correct data and invalid with incorrect data.
-   **URL Tests:** To ensure that all URL endpoints resolve to the correct views.