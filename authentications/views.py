from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UsersRegistrationForm

def register_user(request):
    if request.method == 'POST':
        form = UsersRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UsersRegistrationForm()

    return render(request, 'register.html', {'form': form})




from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsersRegistrationForm
from django.contrib.auth.forms import AuthenticationForm


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")

                # Redirect based on account type
                if user.account_type == 'vendor':
                    return redirect('vendor_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})



from django.contrib.auth import logout
from django.contrib import messages

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login') 



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from pages.models import Product

@login_required
def user_dashboard(request):
    if request.user.account_type != 'user':
        return redirect('vendor_dashboard')  # Redirect if vendor tries to access user dashboard
    return render(request, 'user_dashboard.html')

@login_required
def vendor_dashboard(request):
    products = Product.objects.filter(creator=request.user)
    if request.user.account_type != 'vendor':
        return redirect('user_dashboard')  # Redirect if user tries to access vendor dashboard
    return render(request, 'vendor_dashboard.html', {'products': products})
