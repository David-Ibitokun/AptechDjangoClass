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

def wishList(request):
    return render(request, 'wishList.html')

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

# from django.shortcuts import redirect, get_object_or_404
# from .models import Product, Wishlist


# @login_required(login_url='login')
# def add_to_wishlist(request, product_id):
#     if request.user.is_authenticated:
#         product = get_object_or_404(Product, id=product_id)
#         Wishlist.objects.get_or_create(user=request.user, product=product)
#     return redirect(request.META.get('HTTP_REFERER', 'home'))

# @login_required
# def wishlist_view(request):
#     wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
#     return render(request, 'wishList.html', {'wishlist_items': wishlist_items})

# from django.shortcuts import redirect, get_object_or_404
# from .models import Product, Wishlist

# def remove_from_wishlist(request, product_id):
#     if request.user.is_authenticated:
#         Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
#     return redirect(request.META.get('HTTP_REFERER', 'home'))
