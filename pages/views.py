from django.shortcuts import render
from .models import Product

# Create your views here.
def home(request):    
    product = Product.objects.all()
    # wishList = Wishlist.objects.all()
    return render(request, 'index.html', {'products': product})

def about(request):
    return render(request, 'about.html')

def shop(request):
    return render(request, 'shop.html')

def singleProduct(request):
    return render(request, 'singleProduct.html')

def cart(request):
    return render(request, 'cart.html')

def myAccount(request):
    return render(request, 'myAccount.html')

def page404(request):
    return render(request, 'page404.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def myProfile(request):
    return render(request, 'myProfile.html')

# def wishList(request):
#     return render(request, 'wishList.html')

def page500(request):
    return render(request, 'page500.html')

def page503(request):
    return render(request, 'page503.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Product


@login_required
def product_list(request):
    products = Product.objects.filter(creator=request.user)
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})


# views.py
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Brand


@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
                brand_name = form.cleaned_data.pop('brand_name').strip()
                brand, _ = Brand.objects.get_or_create(name__iexact=brand_name, defaults={'name': brand_name})
                product = form.save(commit=False)
                product.brand = brand
                product.creator = request.user
                product.save()
                form.save_m2m()
                return redirect('product_list')
    else:
        form = ProductForm()
        return render(request, 'add_product.html', {'form': form})

# views.py
from .models import Brand, Product

def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'brand_list.html', {'brands': brands})

def brand_detail(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    products = Product.objects.filter(brand=brand)
    return render(request, 'brand_detail.html', {'brand': brand, 'products': products})


# views.py (Updated Add to Cart Functionality)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Cart, CartItem, Product, Order, OrderItem

User = get_user_model()

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not product.is_available or product.stock_quantity < 1:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect(request.META.get('HTTP_REFERER', 'cart'))

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect('cart')


@login_required(login_url='login')
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.get_total() for item in items)
    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.cart.user == request.user:
        item.delete()
        messages.success(request, "Item removed from cart.")
    return redirect('cart')

def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    
    order = Order.objects.create(user=request.user, total_price=total)
    for item in items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
    
    cart.delete()  # clear the cart after checkout
    return render(request, 'checkout_complete.html', {'order': order})

def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    
    order = Order.objects.create(user=request.user, total_price=total)
    for item in items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
    
    cart.delete()  # clear the cart after checkout
    return render(request, 'checkout_complete.html', {'order': order})



# views.py

from django.db.models import Q

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()
    
    return render(request, 'search.html', {'products': products})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Wishlist, Product

# @login_required
# def add_to_wishlist(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     try:
#         Wishlist.objects.get_or_create(user=request.user, product=product)
#         messages.success(request, f"{product.name} added to your wishlist.")
#     except Exception as e:
#         messages.error(request, f"Error adding to wishlist: {str(e)}")

#     return redirect(request.META.get('HTTP_REFERER', 'wishlist'))


from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Product, Wishlist
from django.contrib.auth.decorators import login_required

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        _, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if created:
            messages.success(request, f"✅ '{product.name}' added to your wishlist.")
        else:
            messages.info(request, f"ℹ️ '{product.name}' is already in your wishlist.")
    except Exception as e:
        messages.error(request, f"❌ Error adding to wishlist: {str(e)}")

    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))



@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    messages.success(request, "Item removed from your wishlist.")
    return redirect('wishlist')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'store/search.html', {'products': products})



@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    
    order = Order.objects.create(user=request.user, total_price=total)
    for item in items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
    
    cart.delete()  # clear the cart after checkout
    return render(request, 'checkout.html', {'order': order, 'user': request.user})



