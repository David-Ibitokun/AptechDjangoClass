# your_app_name/forms.py

from django import forms
from .models import Product, Category, Brand # Make sure Product, Category, Brand are imported
from taggit.forms import TagField
from django_select2.forms import Select2TagWidget

class ProductForm(forms.ModelForm):
    # Custom field for brand name, which will be used to get_or_create Brand instance
    brand_name = forms.CharField(
        label="Brand Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter brand name'}),
        required=True
    )

    # Django's ModelChoiceField will render a <select> dropdown for categories
    # We keep this for validation purposes, even if the template renders it manually.
    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'),
        empty_label="--- Select a Category ---",
        widget=forms.Select(attrs={'class': 'form-control'}), # This widget is a <select>
        required=True,
        label="Product Category"
    )

    # TagField integrated with django-taggit and styled with django-select2
    tags = TagField(
        required=False,
        widget=Select2TagWidget(attrs={
            'data-tags': 'true',  # Essential for allowing users to create new tags
            'class': 'form-control',
            'placeholder': 'Enter tags like #trendy, #clothes'
        }),
        help_text='Start typing and select existing tags or create new ones, separated by commas.'
    )

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'discount_price',
            'image',
            'stock_quantity',
            'is_available',
            'category', # Include category in fields (for validation)
            'tags',     # Include tags in fields
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide a detailed description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 99.99'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Optional: e.g., 79.99'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply 'form-control' class to all text/number/select inputs by default
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, Select2TagWidget)):
                current_class = field.widget.attrs.get('class', '')
                if 'form-control' not in current_class:
                    field.widget.attrs['class'] = (current_class + ' form-control').strip()
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input' # Ensure checkboxes have this class
            # Select2TagWidget already has its class defined in its attrs

        # If editing an existing product, populate the brand_name field from the instance's brand
        if self.instance and self.instance.brand:
            self.initial['brand_name'] = self.instance.brand.name

    def save(self, commit=True):
        # Save the form without committing to the database yet, so we can modify the instance
        product = super().save(commit=False)

        # Handle the custom brand_name field
        brand_name = self.cleaned_data.get('brand_name')
        if brand_name:
            # Get or create the Brand object based on the provided name
            brand, _ = Brand.objects.get_or_create(name=brand_name.strip())
            product.brand = brand
        else:
            # If no brand name is provided, set brand to None (if your model allows null brand)
            product.brand = None

        if commit:
            # Save the product instance to the database
            product.save()
            # Save ManyToMany relations (like tags) if commit=True
            self.save_m2m()
        return product