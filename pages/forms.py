from django import forms
from .models import Product, Category, Brand

class ProductForm(forms.ModelForm):
    name = forms.CharField(
    label="Product Name",
    max_length=255,
    widget=forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Enter product name'
    })
    )

    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe the product'
        })
    )

    price = forms.DecimalField(
        label="Price",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    discount_price = forms.DecimalField(
        label="Discount Price",
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    categories = forms.ModelMultipleChoiceField(
    label="Categories",
    queryset=Category.objects.all(),
    widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    brand_name = forms.CharField(
        label="Brand",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter brand name'}),
        required=True
    )

    tags = forms.CharField(
        label="Tags",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Comma-separated tags (e.g. casual, summer)'
        })
    )

    image = forms.ImageField(
        label="Product Image",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    stock_quantity = forms.IntegerField(
        label="Stock Quantity",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    is_available = forms.BooleanField(
        label="Is Available?",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Product
        exclude = ['slug', 'creator', 'created_at', 'updated_at', 'brand']



