



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, F
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db import IntegrityError # Import for database errors

from .models import Product, Category, Brand, Cart, CartItem, Wishlist, Order, OrderItem
from .forms import ProductForm

User = get_user_model() # Get the currently active user model

# --- Public Facing Views ---



def home(request):
    """
    Renders the homepage with latest products and parent categories.
    """
    products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    parent_categories = Category.objects.filter(parent__isnull=True)

    context = {
        'products': products,
        'parent_categories': parent_categories,
    }
    return render(request, 'index.html', context)

def contact(request):
    """
    Renders the contact page.
    You can add form handling logic here later if you create a contact form.
    """
    return render(request, 'contact.html')

def category_detail(request, slug):
    """
    Renders a category detail page, displaying the category's information
    and all products belonging to it or any of its subcategories.
    """
    category = get_object_or_404(Category, slug=slug)

    # Get the current category's ID
    category_ids = [category.id]

    # Recursively get IDs of all subcategories
    # This is a simple recursive approach. For very deep hierarchies,
    # consider a more optimized method or a tree-specific Django package.
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

    return render(request, 'category_detail.html', {
        'category': category,
        'products': products,
        'breadcrumb': breadcrumb,
    })

def about(request):
    """
    Renders the about page.
    """
    return render(request, 'about.html')

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
    context = {
        'product': product
    }
    return render(request, 'brand_detail.html', context)

def view_cart(request):
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

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def myAccount(request):
    """
    Renders the user's account dashboard.
    """
    return render(request, 'my-account.html')

def page404(request):
    """
    Renders the 404 Not Found page.
    """
    return render(request, 'page404.html', status=404)

def login(request):
    """
    Renders the login page. (Authentication logic typically handled by Django's built-in views)
    """
    return render(request, 'login.html')

def register(request):
    """
    Renders the registration page. (Registration logic typically handled by Django's built-in views)
    """
    return render(request, 'register.html')

def myProfile(request):
    """
    Renders the user's profile page.
    """
    return render(request, 'myProfile.html')

def page500(request):
    """
    Renders the 500 Internal Server Error page.
    """
    return render(request, 'page500.html', status=500)

def page503(request):
    """
    Renders the 503 Service Unavailable page.
    """
    return render(request, 'page503.html', status=503)

# --- Vendor/Seller Dashboard Views ---

@login_required(login_url='login')
def product_list(request):
    """
    Displays a list of products created by the logged-in user (vendor dashboard).
    """
    products = Product.objects.filter(creator=request.user).order_by('-created_at')
    context = {
        'products': products
    }
    return render(request, 'product_list.html', context)


@login_required(login_url='login')
def vendor_orders(request):
    """
    Displays a list of orders that contain products created by the logged-in vendor.
    """
    # Get all OrderItems where the product's creator is the current user
    # Use select_related to optimize fetching related Order and Product objects
    vendor_order_items = OrderItem.objects.filter(product__creator=request.user).select_related('order', 'product')

    # Get unique Order objects from these OrderItems
    # This ensures each order is listed only once, even if it contains multiple products from the vendor
    vendor_orders_list = Order.objects.filter(orderitem__in=vendor_order_items).distinct().order_by('-created_at')

    context = {
        'orders': vendor_orders_list,
    }
    return render(request, 'vendor_orders.html', context)

@login_required(login_url='login')
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    category = product.category

    # Build breadcrumb list (from root to current)
    breadcrumb = []
    current = category
    while current:
        breadcrumb.insert(0, current)
        current = current.parent

    return render(request, 'product_detail.html', {
        'product': product,
        'breadcrumb': breadcrumb,
    })


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
                form.save()
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
    product = get_object_or_404(Product, slug=slug, creator=request.user)

    # ADDED / KEPT: top_level_categories and selected_category_id for the custom category accordion
    top_level_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

    selected_category_id = None
    if request.method == 'POST' and 'category' in request.POST:
        try:
            selected_category_id = int(request.POST.get('category'))
        except (TypeError, ValueError):
            selected_category_id = None
    elif product.category: # If initial form render, get category from product instance
        selected_category_id = product.category.id

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # KEPT: Manual category handling for edit
            category_id = request.POST.get('category')
            if category_id:
                try:
                    product.category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    messages.error(request, "Selected category does not exist.")
                    product.category = None
            else:
                product.category = None

            # The form.save() method will now automatically handle the 'brand' field
            # and update the product instance.
            form.save()

            messages.success(request, "Product updated successfully!")
            return redirect('product_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product) # Form will be pre-filled including brand_name

    context = {
        'form': form,
        'product': product,
        # ADDED / KEPT: for category accordion
        'top_level_categories': top_level_categories,
        'selected_category_id': selected_category_id,
    }
    return render(request, 'edit_product.html', context)


def brand_detail(request, slug=None, pk=None): # Modified to accept both slug and pk
    """
    Displays details for a single brand and its products.
    Can be accessed by slug or primary key.
    """
    from django.http import Http404 # Import Http404 here
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


@login_required(login_url='login')
def delete_product(request, slug):
    """
    Handles deleting a product by a vendor.
    """
    # Ensure only the creator can delete their product
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
    context = {
        'brands': brands
    }
    return render(request, 'brand_list.html', context)

def brand_detail(request, slug):
    """
    Displays details for a single brand and its products.
    """
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.filter(brand=brand, is_available=True).order_by('-created_at')
    context = {
        'brand': brand,
        'products': products
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
def checkout(request):
    """
    Handles the checkout process, creating an order from the cart.
    (Note: This version simulates checkout without external payment gateway integration.)
    """
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('home')

    total_price = cart.get_total_price()

    if request.method == 'POST':
        try:
            for item in cart_items:
                if item.quantity > item.product.stock_quantity:
                    messages.error(request, f"Not enough stock for {item.product.name}. Available: {item.product.stock_quantity}, Your cart: {item.quantity}")
                    return redirect('cart')

            order = Order.objects.create(user=user, total_price=total_price, is_paid=True)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.get_display_price()
                )
                item.product.stock_quantity -= item.quantity
                item.product.save()

            cart_items.delete()
            messages.success(request, "Your order has been placed successfully!")
            return render(request, 'checkout_complete.html', {'order': order})
        except Exception as e:
            messages.error(request, f"An error occurred during checkout: {e}")
            return redirect('checkout')

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'checkout.html', context)


# --- Search Functionality ---

def search(request):
    """
    Enhanced search view: allows searching by name, description,
    category name, brand name, and tags.
    """
    query = request.GET.get('q')
    products = Product.objects.none()
    category_id = request.GET.get('category', '')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(brand__name__icontains=query)
        ).distinct()

    if category_id:
        # Assuming category_id refers to a parent category to filter products by its children
        products = products.filter(category__parent__id=category_id)

    return render(request, 'search_results.html', {
        'query': query,
        'products': products
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
    # Ensure this line is correctly indented (4 spaces from 'def')
    try:
        wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
        product_name = wishlist_item.product.name
        wishlist_item.delete()
        messages.info(request, f"{product_name} removed from your wishlist.")
    except Exception as e: # Catch any potential errors, though get_object_or_404 handles 404s
        messages.error(request, f"Error removing item from wishlist: {e}")
    return redirect('wishlist')


@login_required(login_url='login') # Corrected: login_url='login'
def wishlist_view(request):
    """
    Displays the user's wishlist.
    """
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-added_at')
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist.html', context)


@login_required(login_url='login')
def recent_order(request):
    """
    Displays a list of recent orders for the logged-in user.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at') # Most recent first
    context = {
        'orders': orders,
    }
    return render(request, 'recent_orders.html', context)