# your_app_name/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, F
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db import IntegrityError
from django.http import Http404

# Import Django's built-in views for password change
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .models import Product, Category, Brand, Cart, CartItem, Wishlist, Order, OrderItem

User = get_user_model()

# --- Public Facing Views ---

def home(request):
    """
    Renders the homepage with latest products and parent categories.
    """
    products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    parent_categories = Category.objects.filter(parent__isnull=True)

    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    context = {
        'products': products,
        'parent_categories': parent_categories,
        'top_level_categories': top_level_categories, # Pass for base.html
    }
    return render(request, 'index.html', context)

def contact(request):
    """
    Renders the contact page.
    You can add form handling logic here later if you create a contact form.
    """
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    return render(request, 'contact.html', {'top_level_categories': top_level_categories})

def category_detail(request, slug):
    """
    Renders a category detail page, displaying the category's information
    and all products belonging to it or any of its subcategories.
    """
    category = get_object_or_404(Category, slug=slug)

    # Get the current category's ID
    category_ids = [category.id]

    # Recursively get IDs of all subcategories
    def get_descendant_ids(current_category):
        ids = []
        for subcat in current_category.subcategories.all():
            ids.append(subcat.id)
            ids.extend(get_descendant_ids(subcat)) # Recursively get sub-subcategories
        return ids

    category_ids.extend(get_descendant_ids(category))

    # Filter products by all collected category IDs
    products = Product.objects.filter(category__id__in=category_ids, is_available=True).order_by('name')

    # Build breadcrumb list (from root to current)
    breadcrumb = []
    current = category
    while current:
        breadcrumb.insert(0, current)
        current = current.parent
    
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    return render(request, 'category_detail.html', {
        'category': category,
        'products': products,
        'breadcrumb': breadcrumb,
        'top_level_categories': top_level_categories, # Pass for base.html
    })

def about(request):
    """
    Renders the about page.
    """
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    return render(request, 'about.html', {'top_level_categories': top_level_categories})

def shop(request):
    """
    Renders the shop page, displaying all available products.
    """
    products = Product.objects.filter(is_available=True).order_by('name')
    
    # Get top-level categories for the main display
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    
    context = {
        'products': products,
        'top_level_categories': top_level_categories, # Pass top-level categories
    }
    return render(request, 'shop.html', context)

def singleProduct(request, slug):
    """
    Renders a single product detail page.
    """
    product = get_object_or_404(Product, slug=slug, is_available=True)
    
    # Build breadcrumb (assuming Category model has parent field and get_absolute_url)
    breadcrumb = []
    current_category = product.category
    while current_category:
        breadcrumb.insert(0, current_category)
        current_category = current_category.parent

    # Example for related products (adjust logic as needed)
    related_products = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(pk=product.pk).order_by('?')[:4] # Exclude current product, get 4 random

    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    context = {
        'product': product,
        'breadcrumb': breadcrumb,
        'products': related_products, # Pass related products for "You might also like"
        'top_level_categories': top_level_categories, # Pass for base.html
    }
    return render(request, 'single-product.html', context)

def cart(request):
    """
    Renders the user's cart page, displaying all items.
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart).order_by('product__name')
        total_price = cart.get_total_price()
    else:
        cart_items = []
        total_price = 0
    
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'top_level_categories': top_level_categories, # Pass for base.html
    }
    return render(request, 'cart.html', context)

def myAccount(request):
    """
    Renders the user's account dashboard.
    """
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    return render(request, 'my-account.html', {'top_level_categories': top_level_categories})

def page404(request):
    """
    Renders the 404 Not Found page.
    """
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    return render(request, '404.html', status=404, context={'top_level_categories': top_level_categories}) # Corrected template name

def login(request):
    """
    Renders the login page. (Authentication logic typically handled by Django's built-in views)
    """
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    return render(request, 'login.html', {'top_level_categories': top_level_categories})

def register(request):
    """
    Renders the registration page. (Registration logic typically handled by Django's built-in views)
    """
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    return render(request, 'register.html', {'top_level_categories': top_level_categories})

@login_required(login_url='login')
def myProfile(request):
    """
    Handles displaying and updating the user's profile information.
    """
    if request.method == 'POST':
        from .forms import UserProfileForm # Import here to avoid circular dependency
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('myProfile') # Redirect to the same page to show updated info
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        from .forms import UserProfileForm # Import here
        form = UserProfileForm(instance=request.user)
    
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    context = {
        'form': form,
        'top_level_categories': top_level_categories, # Pass for base.html
    }
    return render(request, 'myProfile.html', context)

# NEW: Password Change Done View (simple redirect or render success message)
@login_required(login_url='login')
def password_change_done(request):
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    return render(request, 'password_change_done.html', {'top_level_categories': top_level_categories})


def page500(request):
    """
    Renders the 500 Internal Server Error page.
    """
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    return render(request, '500.html', status=500, context={'top_level_categories': top_level_categories})

def page503(request):
    """
    Renders the 503 Service Unavailable page.
    """
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    return render(request, '503.html', status=503, context={'top_level_categories': top_level_categories})


@login_required(login_url='login')
def recent_order(request):
    """
    Displays a list of recent orders for the logged-in user.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at') # Most recent first
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    context = {
        'orders': orders,
        'top_level_categories': top_level_categories, # Pass for base.html
    }
    return render(request, 'recent_orders.html', context)

@login_required(login_url='login')
def order_detail(request, order_number): # Changed parameter name to order_number
    """
    Displays the details of a specific order for the logged-in user.
    """
    # --- DEBUGGING PRINTS ---
    print(f"DEBUG: order_detail view called.")
    print(f"DEBUG: order_number from URL: '{order_number}' (type: {type(order_number)})")
    print(f"DEBUG: Current logged-in user: {request.user.username} (ID: {request.user.id})")
    print(f"DEBUG: Is user authenticated? {request.user.is_authenticated}")
    # --- END DEBUGGING PRINTS ---

    # Ensure the order belongs to the logged-in user for security
    order = get_object_or_404(Order, order_number=order_number, user=request.user) # Query by order_number
    
    # Get all order items related to this order
    order_items = OrderItem.objects.filter(order=order).select_related('product')
    
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    context = {
        'order': order,
        'order_items': order_items, # Pass order items
        'top_level_categories': top_level_categories, # Pass for base.html
    }
    return render(request, 'order_detail.html', context)


@login_required(login_url='login')
def users_order_detail(request, order_number):
    """
    Displays the details of a specific order for the logged-in user.
    """
    # Ensures the order belongs to the logged-in user for security
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    order_items = OrderItem.objects.filter(order=order).select_related('product')
    
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    context = {
        'order': order,
        'order_items': order_items,
        'top_level_categories': top_level_categories,
    }
    return render(request, 'users_order_detail.html', context)

@login_required(login_url='login')
def user_dashboard(request, order_number):
    """
    Renders the user dashboard page.
    """
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    return render(request, 'user_dashboard.html', {'top_level_categories': top_level_categories})


# --- Vendor/Seller Dashboard Views ---

@login_required(login_url='login')
def product_list(request):
    """
    Displays a list of products created by the logged-in user (vendor dashboard).
    """
    products = Product.objects.filter(creator=request.user).order_by('-created_at')
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    context = {
        'products': products,
        'top_level_categories': top_level_categories, # Pass for base.html
    }
    return render(request, 'product_list.html', context)


@login_required(login_url='login')
def vendor_orders(request):
    """
    Displays a list of orders that contain products created by the logged-in vendor.
    """
    # Get all OrderItems where the product's creator is the current user
    # Use select_related to optimize fetching related Order and Product objects
    # Also select_related('user') to get customer details efficiently
    vendor_orders_list = Order.objects.filter(orderitem__product__creator=request.user)\
                                      .distinct()\
                                      .select_related('user')\
                                      .annotate(
                                          vendor_total_amount=Sum(
                                              F('orderitem__quantity') * F('orderitem__price_at_purchase'),
                                              filter=Q(orderitem__product__creator=request.user)
                                          )
                                      ).order_by('-created_at')

    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    context = {
        'orders': vendor_orders_list,
        'top_level_categories': top_level_categories,
    }
    return render(request, 'vendor_orders.html', context)



@login_required(login_url='login')
def vendor_order_detail(request, order_number): # Changed parameter name to order_number
    """
    Displays details of a specific order for the vendor,
    showing only the products supplied by this vendor.
    """
    # --- DEBUGGING PRINTS ---
    print(f"DEBUG: vendor_order_detail view called.")
    print(f"DEBUG: order_number from URL: '{order_number}' (type: {type(order_number)})")
    print(f"DEBUG: Current logged-in vendor user: {request.user.username} (ID: {request.user.id})")
    print(f"DEBUG: Is vendor authenticated? {request.user.is_authenticated}")
    # --- END DEBUGGING PRINTS ---

    order = get_object_or_404(Order, order_number=order_number) # Query by order_number

    # Filter order items to only include products created by the current vendor
    vendor_order_items = OrderItem.objects.filter(
        order=order,
        product__creator=request.user
    ).select_related('product') # Eager load product for efficiency

    # Calculate the total for this vendor's items in this specific order
    vendor_total_price = sum(item.get_total_price() for item in vendor_order_items)

    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    context = {
        'order': order,
        'vendor_order_items': vendor_order_items,
        'vendor_total_price': vendor_total_price,
        'top_level_categories': top_level_categories,
    }
    return render(request, 'order_detail.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug) # No is_available filter here, useful for vendor to see all
    category = product.category

    # Build breadcrumb list (from root to current)
    breadcrumb = []
    current = category
    while current:
        breadcrumb.insert(0, current)
        current = current.parent
    
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    # --- Start: Logic for "You might also like" products ---
    related_products = Product.objects.filter(
        category=product.category, # Same category
        is_available=True # Only show available products
    ).exclude(pk=product.pk).order_by('?')[:4] # Exclude current product, get 4 random
    # --- End: Logic for "You might also like" products ---

    context = {
        'product': product,
        'breadcrumb': breadcrumb,
        'top_level_categories': top_level_categories, # Pass for base.html
        'products': related_products, # <-- NEW: Pass related products for "You might also like" section
    }
    return render(request, 'product_detail.html', context)


def generate_unique_slug(name):
    base_slug = slugify(name)
    slug = base_slug
    counter = 1
    while Product.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


@login_required(login_url='login')
def add_product(request):
    from .forms import ProductForm
    form = ProductForm(request.POST or None, request.FILES or None)
    top_level_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

    selected_category_id = None
    if request.method == 'POST' and 'category' in request.POST:
        try:
            selected_category_id = int(request.POST.get('category'))
        except (TypeError, ValueError):
            selected_category_id = None

    if request.method == 'POST':
        if form.is_valid():
            product = form.save(commit=False) # This already sets product.brand via form's save method

            if request.user.is_authenticated:
                product.creator = request.user
            else:
                messages.error(request, "Authentication required to add a product. Please log in again.")
                return redirect('login')

            # Manual category handling for accordion style
            category_id = request.POST.get('category')
            if category_id:
                try:
                    product.category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    messages.error(request, "Selected category does not exist.")
                    product.category = None # Set to None if it's optional
            else:
                product.category = None # Ensure it's explicitly None if not selected and allowed

            try:
                form.save() # This will save the product instance and its ManyToMany fields (like tags)
                messages.success(request, f"Product '{product.name}' added successfully!")
                return redirect('product_list')
            except IntegrityError as e:
                messages.error(request, f"A product with that name or slug might already exist, or another database error occurred: {e}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred while saving the product: {e}")
        else:
            messages.error(request, "Please correct the errors in the form.")

    context = {
        'form': form,
        'top_level_categories': top_level_categories,
        'selected_category_id': selected_category_id,
    }
    return render(request, 'add_product.html', context)


@login_required(login_url='login')
def edit_product(request, slug):
    from .forms import ProductForm
    product = get_object_or_404(Product, slug=slug, creator=request.user)
    top_level_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
    selected_category_id = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Handle category selection manually before saving the form
            category_id = request.POST.get('category')
            if category_id:
                try:
                    product.category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    messages.error(request, "Selected category does not exist.")
                    product.category = None # Set to None if invalid
            else:
                product.category = None # Set to None if no category selected

            # Save the form. This will save the product instance AND its ManyToMany fields (like tags).
            # Since we've already set product.category on the instance, it will also save that.
            form.save() # This is the corrected line.

            messages.success(request, "Product updated successfully!")
            return redirect('product_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)
        # For GET request, if product has a category, set selected_category_id for template
        if product.category:
            selected_category_id = product.category.id

    context = {
        'form': form,
        'product': product, # Pass product to the template for image preview etc.
        'top_level_categories': top_level_categories,
        'selected_category_id': selected_category_id,
    }
    return render(request, 'edit_product.html', context)

@login_required(login_url='login')
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug, creator=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('product_list')
    context = {
        'product': product
    }
    return render(request, 'delete_product_confirm.html', context)

# --- Brand Views ---

def brand_list(request):
    """
    Displays a list of all brands.
    """
    brands = Brand.objects.all().order_by('name')
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    context = {
        'brands': brands,
        'top_level_categories': top_level_categories, # Pass for base.html
    }
    return render(request, 'brand_list.html', context)

def brand_detail(request, slug=None, pk=None): # Modified to accept both slug and pk
    """
    Displays details for a single brand and its products.
    Can be accessed by slug or primary key.
    """
    if slug:
        brand = get_object_or_404(Brand, slug=slug)
    elif pk:
        brand = get_object_or_404(Brand, pk=pk)
    else:
        # This case should ideally not be reached if URL patterns are set up correctly
        # but as a fallback, raise a 404 or redirect
        raise Http404("No brand identifier provided.") # Import Http404 if needed

    products = Product.objects.filter(brand=brand, is_available=True).order_by('-created_at')
    
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    context = {
        'brand': brand,
        'products': products,
        'top_level_categories': top_level_categories, # Pass for base.html
    }
    return render(request, 'brand_detail.html', context)

# --- Cart Management ---

@login_required(login_url='login')
def add_to_cart(request, product_id):
    """
    Adds a product to the user's cart or increments its quantity from the submitted form.
    """
    product = get_object_or_404(Product, id=product_id)

    if not product.is_available or product.stock_quantity == 0:
        messages.error(request, f"{product.name} is currently out of stock or unavailable.")
        return redirect(request.META.get('HTTP_REFERER', 'shop'))

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            raise ValueError
    except (TypeError, ValueError):
        messages.error(request, "Invalid quantity selected.")
        return redirect(request.META.get('HTTP_REFERER', 'shop'))

    if quantity > product.stock_quantity:
        messages.error(request, f"Only {product.stock_quantity} units of {product.name} available.")
        return redirect(request.META.get('HTTP_REFERER', 'shop'))

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        total_quantity = cart_item.quantity + quantity
        if total_quantity > product.stock_quantity:
            available_to_add = product.stock_quantity - cart_item.quantity
            messages.warning(request, f"You can only add {available_to_add} more of {product.name}.") # Corrected variable name
            return redirect(request.META.get('HTTP_REFERER', 'shop'))
        cart_item.quantity = total_quantity
        cart_item.save()
        messages.success(request, f"Updated {product.name} quantity to {cart_item.quantity}.")
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"{product.name} added to your cart.")

    return redirect(request.META.get('HTTP_REFERER', 'shop'))


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    """
    Removes a product from the user's cart.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f"{product_name} removed from your cart.")
    return redirect('cart')

@login_required(login_url='login')
def update_cart_quantity(request, item_id):
    """
    Updates the quantity of a product in the user's cart.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        try:
            new_quantity = int(request.POST.get('quantity', 1))
            if new_quantity <= 0:
                messages.error(request, "Quantity must be at least 1.")
                return redirect('cart')

            if new_quantity > cart_item.product.stock_quantity:
                messages.error(request, f"Cannot update quantity for {cart_item.product.name}. Only {cart_item.product.stock_quantity} available.")
                return redirect('cart')

            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f"Quantity for {cart_item.product.name} updated.")
        except ValueError:
            messages.error(request, "Invalid quantity.")
    return redirect('cart')

@login_required(login_url='login')
def view_cart(request): # This is a duplicate of `cart` view, consider removing one.
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.get_total_price() for item in items)
    
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    return render(request, 'cart.html', {
        'cart_items': items, # Changed from 'items' to 'cart_items' for consistency with checkout.html
        'total_price': total, # Changed from 'total' to 'total_price'
        'top_level_categories': top_level_categories, # Pass for base.html
    })


@login_required(login_url='login')
def checkout(request):
    """
    Handles the checkout process, creating an order from the cart,
    and then rendering the order confirmation directly.
    """
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('shop') # Redirect to shop if cart is empty

    total_price = cart.get_total_price()

    if request.method == 'POST':
        # Basic validation for shipping fields (can be replaced by a proper form)
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        phone_number = request.POST.get('phone_number')
        payment_method = request.POST.get('payment_method')

        if not all([address, city, country, payment_method]):
            messages.error(request, "Please fill in all required shipping details and select a payment method.")
            context = {
                'cart': cart,
                'cart_items': cart_items,
                'total_price': total_price,
                'top_level_categories': top_level_categories,
                # Pass back submitted data to pre-fill form if validation fails
                'address': address, 'city': city, 'zip_code': zip_code, 'country': country,
                'phone_number': phone_number,
                'payment_method': payment_method,
            }
            return render(request, 'checkout.html', context)

        try:
            # Re-check stock before finalizing
            for item in cart_items:
                # Refresh product from DB to get latest stock info
                product = Product.objects.get(id=item.product.id)
                if item.quantity > product.stock_quantity:
                    messages.error(request, f"Not enough stock for {product.name}. Available: {product.stock_quantity}, Your cart: {item.quantity}. Please adjust your cart.")
                    return redirect('cart') # Redirect back to cart to allow adjustment

            # Create the Order
            order = Order.objects.create(
                user=user,
                total_price=total_price,
                is_paid=True, # Assuming COD or simulated instant payment
                address=address,
                city=city,
                zip_code=zip_code,
                phone_number = phone_number,
                country=country,
                payment_method=payment_method,
            )
            # The order.save() method (from models.py) will automatically generate order_number here

            # Create OrderItems and update product stock
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.get_display_price() # Use get_display_price for consistency
                )
                item.product.stock_quantity -= item.quantity
                item.product.save()

            # Clear the user's cart
            cart_items.delete()
            cart.delete() # Optionally delete the cart itself if it's no longer needed

            messages.success(request, "Your order has been placed successfully!")
            # Render checkout_complete.html directly instead of redirecting
            context = {
                'order': order,
                'top_level_categories': top_level_categories, # Pass for base.html
            }
            return render(request, 'checkout.html', context)
        except Exception as e:
            messages.error(request, f"An unexpected error occurred during checkout: {e}")
            # If an error occurs, render the checkout page again with current context
            context = {
                'cart': cart,
                'cart_items': cart_items,
                'total_price': total_price,
                'top_level_categories': top_level_categories,
                # Pass back submitted data to pre-fill form
                'address': address, 'city': city, 'zip_code': zip_code, 'country': country,
                'phone_number' : phone_number,
                'payment_method': payment_method,
            }
            return render(request, 'checkout.html', context)
    else:
        # GET request: Display the checkout form
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price,
            'top_level_categories': top_level_categories, # Pass for base.html
            # Pre-fill shipping info from user profile if available
            'address': user.address if hasattr(user, 'address') else '',
            'city': user.city if hasattr(user, 'city') else '',
            'zip_code': user.zip_code if hasattr(user, 'zip_code') else '',
            'country': user.country if hasattr(user, 'country') else '',
            'phone_number': user.phone_number if hasattr(user, 'phone_number') else '',
            'payment_method': 'COD', # Default selected payment method
        }
        return render(request, 'checkout.html', context)

# Removed checkout_complete view as it's now integrated into the checkout view
# @login_required(login_url='login')
# def checkout_complete(request, order_id):
#     """
#     Displays the order confirmation page.
#     """
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     # Get top-level categories for the base template's navigation
#     top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
#     context = {
#         'order': order,
#         'top_level_categories': top_level_categories, # Pass for base.html
#     }
#     return render(request, 'checkout_complete.html', context)


# --- Search Functionality ---

def search(request):
    """
    Enhanced search view: allows searching by name, description,
    category name, brand name, and tags.
    """
    query = request.GET.get('q')
    products = Product.objects.none()
    category_id = request.GET.get('category', '') # This is the ID of the selected category

    # Get top-level categories for the search form's dropdown
    top_level_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(brand__name__icontains=query)
        ).distinct()

    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id)
            # Get IDs of the selected category and all its descendants
            category_ids_to_filter = [selected_category.id]
            def get_descendant_ids(current_category):
                ids = []
                for subcat in current_category.subcategories.all():
                    ids.append(subcat.id)
                    ids.extend(get_descendant_ids(subcat))
                return ids
            category_ids_to_filter.extend(get_descendant_ids(selected_category))
            
            # Filter products by all collected category IDs
            products = products.filter(category__id__in=category_ids_to_filter)
        except Category.DoesNotExist:
            pass # If category_id is invalid, just ignore the filter

    return render(request, 'search_results.html', {
        'query': query,
        'products': products,
        'top_level_categories': top_level_categories, # Pass for search form
        'selected_category_id': category_id, # Pass to pre-select dropdown
    })


# --- Wishlist Management ---

@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    """
    Adds a product to the user's wishlist.
    """
    product = get_object_or_404(Product, id=product_id)
    try:
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if created:
            messages.success(request, f"{product.name} added to your wishlist!")
        else:
            messages.info(request, f"{product.name} is already in your wishlist.")
    except Exception as e:
        messages.error(request, f"Could not add {product.name} to wishlist: {e}")
    return redirect(request.META.get('HTTP_REFERER', 'wishlist_view'))



@login_required(login_url='login')
def remove_from_wishlist(request, item_id):
    """
    Removes a product from the user's wishlist.
    """
    try:
        wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
        product_name = wishlist_item.product.name
        wishlist_item.delete()
        messages.info(request, f"{product_name} removed from your wishlist.")
    except Exception as e: # Catch any potential errors, though get_object_or_404 handles 404s
        messages.error(request, f"Error removing item from wishlist: {e}")
    return redirect('wishlist_view')


@login_required(login_url='login') # Corrected: login_url='login'
def wishlist_view(request):
    """
    Displays the user's wishlist.
    """
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-added_at')
    # Get top-level categories for the base template's navigation
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    context = {
        'wishlist_items': wishlist_items,
        'top_level_categories': top_level_categories, # Pass for base.html
    }
    return render(request, 'wishlist.html', context)
