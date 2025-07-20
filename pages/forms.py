# Assuming this is in your forms.py (e.g., products/forms.py or similar)
from django import forms
from .models import Product, Category, Brand # Make sure Brand is imported
from taggit.forms import TagWidget # Import TagWidget if you are using django-taggit

class ProductForm(forms.ModelForm):
    # This field handles creating/selecting the Brand name from user input.
    # It will be used to get_or_create a Brand instance in the form's save method.
    brand_name = forms.CharField(
        label="Brand Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter brand name'}),
        required=True
    )

    # This field is now ModelChoiceField for single category selection.
    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'), # Show ALL categories, sorted by name
        empty_label="--- Select a Category ---", # Adds a default empty option
        widget=forms.Select(attrs={'class': 'form-control'}), # Standard dropdown widget
        required=True, # Set to False if a product category is optional
        label="Product Category"
    )

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'discount_price',
            'image',
            'stock_quantity', # Correct field name
            'is_available',
            'category',
            'tags'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide a detailed description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 99.99'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Optional: e.g., 79.99'}),
            # 'brand' widget is now completely removed as 'brand_name' is used
            'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': 'Comma-separated tags'}), # Use TagWidget
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}), # CORRECTED FIELD NAME HERE
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'tags': 'Separate tags with commas.',
            'is_available': 'Check if the product should be visible on the store.',
            'stock_quantity': 'Number of items available in stock.', # Add help text for clarity
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply 'form-control' class to most input fields for consistent styling
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                current_class = field.widget.attrs.get('class', '')
                if 'form-control' not in current_class:
                    field.widget.attrs['class'] = (current_class + ' form-control').strip()
            else: # For CheckboxInput
                field.widget.attrs['class'] = 'form-check-input'

        # If editing an existing product, populate the 'brand_name' field from the instance
        if self.instance and self.instance.brand:
            self.initial['brand_name'] = self.instance.brand.name

    def save(self, commit=True):
        product = super().save(commit=False)

        brand_name = self.cleaned_data.get('brand_name')
        if brand_name:
            brand, created = Brand.objects.get_or_create(name=brand_name.strip())
            product.brand = brand
        else:
            product.brand = None

        if commit:
            product.save()
            self.save_m2m() # This is still needed for 'tags' (django-taggit)

        return product