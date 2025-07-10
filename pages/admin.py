from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'category', 
        'price', 
        'discount_price', 
        'stock_quantity', 
        'is_available', 
        'creator', 
        'created_at'
    )
    search_fields = ('name', 'category', 'tags')
    list_filter = ('category', 'is_available', 'created_at')
    ordering = ('-created_at',)
