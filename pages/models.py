from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager # For django-taggit

User = get_user_model() # Get the currently active user model

# --- Core E-commerce Models ---

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        """
        Custom save method to auto-generate a unique slug from the category name.
        If a slug already exists, it appends a number to ensure uniqueness.
        """
        if not self.slug: # Only generate slug if it's not already set
            original_slug = slugify(self.name)
            queryset = Category.objects.all()

            # Exclude the current instance if it's an update, to avoid self-collision checks
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)

            # Check for existing slugs and append a number if necessary
            unique_slug = original_slug
            num = 1
            while queryset.filter(slug=unique_slug).exists():
                unique_slug = f"{original_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Ensure you have a 'category_detail' URL pattern defined in your urls.py
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        if self.parent:
            # Displays as "Parent Category > Child Category"
            return f"{self.parent.name} > {self.name}"
        return self.name # Displays as "Main Category"

    def get_ancestors(self):
        """
        Returns a list of all parent categories leading up to this category,
        ordered from top-level down to the direct parent.
        """
        ancestors = []
        current = self
        while current.parent:
            ancestors.insert(0, current.parent) # Insert at the beginning to maintain order
            current = current.parent
        return ancestors

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Apply the same unique slug generation logic here for Brand
        if not self.slug:
            original_slug = slugify(self.name)
            queryset = Brand.objects.all()

            if self.pk:
                queryset = queryset.exclude(pk=self.pk)

            unique_slug = original_slug
            num = 1
            while queryset.filter(slug=unique_slug).exists():
                unique_slug = f"{original_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/images/')
    stock_quantity = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_products')

    # CHANGED: ForeignKey for single category
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # If a category is deleted, set product's category to NULL
        null=True,                 # Allow category to be null in DB
        blank=True,                # Allow category to be empty in forms
        related_name='products_in_category'
    )

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    tags = TaggableManager(blank=True) # For django-taggit

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Apply the same unique slug generation logic here for Product
        if not self.slug:
            original_slug = slugify(self.name)
            queryset = Product.objects.all()

            if self.pk:
                queryset = queryset.exclude(pk=self.pk)

            unique_slug = original_slug
            num = 1
            while queryset.filter(slug=unique_slug).exists():
                unique_slug = f"{original_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('singleProduct', kwargs={'slug': self.slug})

    def get_discount_percent(self):
        if self.discount_price and self.price:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return round(discount)
        return 0

    def get_display_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.quantity * self.product.get_display_price()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') # A user can only add a product once to wishlist
        ordering = ['-added_at']
        verbose_name_plural = 'Wishlist Items'

    def __str__(self):
        return f"{self.product.name} in {self.user.username}'s wishlist"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False) # For tracking payment status
    # Add fields like shipping address, payment method etc. here for a real app

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} by {self.user.username if self.user else 'Guest'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) # Product can be null if deleted
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2) # Store price at time of order

    def get_total(self):
        return self.quantity * self.price_at_purchase

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'} in Order {self.order.id}"