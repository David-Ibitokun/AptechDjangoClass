# authentications/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsersRegistration

class UsersRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label='First Name',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'})
    )
    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    account_type = forms.ChoiceField(
        label='Account Type',
        choices=UsersRegistration.ACCOUNT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    agreed_to_terms = forms.BooleanField(
        label='I agree to the terms and conditions',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta(UserCreationForm.Meta):
        model = UsersRegistration
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'account_type',
            'agreed_to_terms',
            # password1 and password2 are implicitly included by UserCreationForm.Meta
        )

        # You can set widgets for password fields directly here if you want
        # to ensure the 'form-control' class is applied.
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Create a username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }

    # Remove or comment out the __init__ method if you use the widgets in Meta
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Create a password'})
    #     self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})
    #     self.fields['password'].help_text = ''
    #     self.fields['password2'].help_text = ''