# from django.contrib import admin
# from .models import Product, Category, Brand

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = (
#         'name',
#         'get_categories',
#         'brand',
#         'price',
#         'discount_price',
#         'stock_quantity',
#         'is_available',
#         'creator',
#         'created_at',
#     )
#     search_fields = ('name', 'tags', 'brand__name')
#     list_filter = ('brand', 'is_available', 'created_at')
#     ordering = ('-created_at',)

#     def get_categories(self, obj):
#         return ", ".join([cat.name for cat in obj.categories.all()])
#     get_categories.short_description = 'Categories'

# admin.site.register(Category)
# admin.site.register(Brand)



from django.contrib import admin
from .models import Product, Category, Brand

class ProductInline(admin.TabularInline):
    model = Product.categories.through  # Through model for ManyToManyField
    extra = 0
    verbose_name = "Product"
    verbose_name_plural = "Products"
    readonly_fields = ('product',)
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False  # Prevent adding from here

class ProductInlineByBrand(admin.TabularInline):
    model = Product
    extra = 0
    fields = ('name', 'price', 'stock_quantity', 'is_available')
    readonly_fields = ('name', 'price', 'stock_quantity', 'is_available')
    can_delete = False
    show_change_link = True # allows clicking to edit product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)
    inlines = [ProductInline]

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Number of Products'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)
    inlines = [ProductInlineByBrand]

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Number of Products'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_categories',
        'brand',
        'price',
        'discount_price',
        'stock_quantity',
        'is_available',
        'creator',
        'created_at',
    )
    list_filter = ('brand', 'categories')
    search_fields = ('name', 'tags')

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    get_categories.short_description = 'Categories'

