from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()

class Category(models.Model):
    CATEGORY_CHOICES = [
    ('Women', 'Women'),
    ('Men', 'Men'),
    ('Kids', 'Kids'),
    ('Accessories', 'Accessories'),
    ]
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    categories = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{get_random_string(4)}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return f"{self.discount_price:,.2f}" if self.discount_price else self.price

    def get_discount_percent(self):
        if self.discount_price:
            percentage = ((self.price - self.discount_price) / self.price) * 100
            return f"{percentage:.2f}"
        return None

    def is_in_stock(self):
        return self.stock_quantity > 0
    

# from django.db import models
# from django.contrib.auth import get_user_model
# User = get_user_model()

# class Wishlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'product')
