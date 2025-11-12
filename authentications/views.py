from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UsersRegistrationForm, CustomAuthenticationForm
# Assuming 'pages' is another app and Product is defined there
from pages.models import Product # Ensure this import path is correct for your project structure


def register_user(request):
    """
    Handles user registration.
    - If POST request, attempts to validate and save the new user.
    - If GET request, displays an empty registration form.
    """
    if request.method == 'POST':
        form = UsersRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally, log in the user immediately after registration
            # login(request, user) # Uncomment if you want to auto-login
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login') # Redirect to the login page
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            print(form.errors) # For debugging purposes

    else:
        form = UsersRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    """
    Handles user login.
    - If POST request, attempts to authenticate the user.
    - If GET request, displays the login form.
    """
    if request.user.is_authenticated: # If already logged in, redirect to dashboard
        if request.user.account_type == 'vendor':
            return redirect('vendor_dashboard')
        else:
            return redirect('user_dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
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
            # This message is shown if the form itself is not valid (e.g., empty fields)
            messages.error(request, "Please enter your username and password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_user(request):
    """
    Logs out the current user and redirects to the login page.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


@login_required
def user_dashboard(request):
    """
    Displays the user dashboard. Requires login.
    Redirects to vendor dashboard if the user is a vendor.
    """
    if request.user.account_type != 'user':
        messages.warning(request, "You do not have permission to view this page.")
        return redirect('vendor_dashboard')
    return render(request, 'user_dashboard.html')


@login_required
def vendor_dashboard(request):
    """
    Displays the vendor dashboard and lists products created by the vendor. Requires login.
    Redirects to user dashboard if the user is a regular user.
    """
    if request.user.account_type != 'vendor':
        messages.warning(request, "You do not have permission to view this page.")
        return redirect('user_dashboard')

    products = Product.objects.filter(creator=request.user)
    return render(request, 'vendor_dashboard.html', {'products': products})

@login_required(login_url='login')
def myProfile(request):
    """
    Handles displaying and updating the user's profile information.
    """
    if request.method == 'POST':
        from ..authentications.forms import UsersRegistrationForm # Import here to avoid circular dependency
        form = UsersRegistrationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('myProfile') # Redirect to the same page to show updated info
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        from .forms import UsersRegistrationForm # Import here
        form = UsersRegistrationForm(instance=request.user)
    # from pages.views import Category
    # Get top-level categories for the base template's navigation
    # top_level_categories = Category.objects.filter(parent__isnull=True).order_by('name')

    context = {
        'form': form,
        # 'top_level_categories': top_level_categories, # Pass for base.html
    }
    return render(request, 'myProfile.html', context)
