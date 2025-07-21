# your_app_name/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
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


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {
        'category': category,
        'products': products,
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
    return render(request, '404.html', status=404)

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
    return render(request, 'my-profile.html')

def page500(request):
    """
    Renders the 500 Internal Server Error page.
    """
    return render(request, '500.html', status=500)

def page503(request):
    """
    Renders the 503 Service Unavailable page.
    """
    return render(request, '503.html', status=503)

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
    # RE-ADDED: top_level_categories for the custom category accordion
    top_level_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

    # This will hold the ID of the selected category if the form fails validation,
    # so we can re-select the correct radio button.
    selected_category_id = None
    if request.method == 'POST' and 'category' in request.POST:
        try:
            selected_category_id = int(request.POST.get('category'))
        except (TypeError, ValueError):
            selected_category_id = None


    # --- DEBUGGING PRINTS (KEEP THESE FOR NOW) ---
    print(f"DEBUG VIEWS: User accessing add_product: {request.user}")
    print(f"DEBUG VIEWS: Is authenticated: {request.user.is_authenticated}")
    if request.user.is_authenticated:
        print(f"DEBUG VIEWS: Authenticated User ID: {request.user.id}, Username: {request.user.username}")
    # --- END DEBUGGING PRINTS ---

    if request.method == 'POST':
        if form.is_valid():
            product = form.save(commit=False) # Get the product instance from the form

            # --- DEBUGGING PRINTS (KEEP THESE FOR NOW) ---
            print(f"DEBUG VIEWS: Form is valid. User at save point: {request.user}")
            print(f"DEBUG VIEWS: Is authenticated at save point: {request.user.is_authenticated}")
            # --- END DEBUGGING PRINTS ---

            # THIS IS THE CRUCIAL LINE FOR ASSIGNING THE CREATOR
            if request.user.is_authenticated:
                product.creator = request.user
                print(f"DEBUG VIEWS: Creator assigned to product: {product.creator}")
            else:
                messages.error(request, "Authentication required to add a product. Please log in again.")
                print("DEBUG VIEWS: ERROR - User not authenticated when trying to assign creator.")
                return redirect('login')

            # RE-ADDED: Manual category handling as requested for accordion style
            category_id = request.POST.get('category')
            if category_id:
                try:
                    product.category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    messages.error(request, "Selected category does not exist.")
                    # If category is required in the Product model, you might want to
                    # make the form invalid or redirect with a stronger error here.
                    product.category = None # Set to None if it's optional
            else:
                product.category = None # Ensure it's explicitly None if not selected and allowed

            try:
                # Assign a unique slug before saving (if your Product model doesn't handle it on save)
                if not product.slug:
                    product.slug = generate_unique_slug(product.name)

                product.save() # This saves the product instance with the assigned creator
                form.save_m2m() # This is crucial for saving ManyToMany fields like 'tags'

                messages.success(request, f"Product '{product.name}' added successfully!")
                return redirect('product_list') # Redirect to the vendor's product list page
            except IntegrityError as e:
                messages.error(request, f"A product with that name or slug might already exist, or another database error occurred: {e}")
                print(f"DEBUG VIEWS: IntegrityError saving product: {e}")
            except Exception as e: # Catch any other unexpected errors during save
                messages.error(request, f"An unexpected error occurred while saving the product: {e}")
                print(f"DEBUG VIEWS: General error saving product: {e}")
        else:
            # If form is not valid, print errors for debugging
            print(f"DEBUG VIEWS: Form is NOT valid. Errors: {form.errors.as_json()}")
            messages.error(request, "Please correct the errors in the form.")

    context = {
        'form': form,
        'top_level_categories': top_level_categories, # RE-ADDED to context
        'selected_category_id': selected_category_id, # Pass for re-selecting radio button
    }
    return render(request, 'add_product.html', context)


@login_required(login_url='login')
def edit_product(request, slug):
    """
    Handles editing an existing product by a vendor.
    """
    # Ensure only the creator can edit their product
    product = get_object_or_404(Product, slug=slug, creator=request.user) 
    
    # RE-ADDED: top_level_categories for the custom category accordion in edit_product
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
            # Manually handle category for edit as well, matching add_product's behavior
            category_id = request.POST.get('category')
            if category_id:
                try:
                    product.category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    messages.error(request, "Selected category does not exist.")
                    product.category = None
            else:
                product.category = None

            product.save() # Save the product instance with the updated category
            form.save_m2m() # Save ManyToMany fields like tags

            messages.success(request, "Product updated successfully!")
            return redirect('product_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'top_level_categories': top_level_categories, # RE-ADDED to context
        'selected_category_id': selected_category_id, # Pass for re-selecting radio button
    }
    return render(request, 'edit_product.html', context)


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
            messages.warning(request, f"You can only add {available_item_to_add} more of {product.name}.")
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
    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


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
        return redirect('shop')

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
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    product_name = wishlist_item.product.name
    wishlist_item.delete()
    messages.info(request, f"{product_name} removed from your wishlist.")
    return redirect('wishlist_view')

@login_required(login_url='login')
def wishlist_view(request):
    """
    Displays the user's wishlist.
    """
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-added_at')
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist.html', context)