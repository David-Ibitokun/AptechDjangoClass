from django.shortcuts import render
from .models import Product

# Create your views here.
def home(request):    
    product = Product.objects.all()
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

@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.creator = request.user
            product.save()
            return redirect('product_list')  # Replace with your product list view name
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product

@login_required
def product_list(request):
    products = Product.objects.filter(creator=request.user)
    return render(request, 'product_list.html', {'products': products})

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})
