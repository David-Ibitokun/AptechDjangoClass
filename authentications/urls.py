from django.urls import path
from .views import (register_user, login_user, user_dashboard, vendor_dashboard, logout_user, 
)

urlpatterns = [ 
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    
    # Dashboard URLs
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('dashboard/vendor/', vendor_dashboard, name='vendor_dashboard'),
]