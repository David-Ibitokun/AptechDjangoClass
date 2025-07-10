from django.contrib import admin
from .models import UsersRegistration

@admin.register(UsersRegistration)
class UsersRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'account_type', 
        'is_active', 
        'is_staff', 
        'date_joined'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('account_type', 'is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)
