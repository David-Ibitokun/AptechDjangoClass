# authentications/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class UsersRegistration(AbstractUser):
    # ... (existing fields like ACCOUNT_CHOICES and account_type) ...

    ACCOUNT_CHOICES = [
        ('user', 'User'),
        ('vendor', 'Vendor'),
    ]
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_CHOICES,
        default='user',
        verbose_name='Account Type'
    )

    # ADD THIS FIELD:
    agreed_to_terms = models.BooleanField(
        default=False, # It's good practice to have a default value
        verbose_name='Agreed to Terms and Conditions'
    )

    class Meta:
        verbose_name = 'User Registration'
        verbose_name_plural = 'Users Registrations'

    def __str__(self):
        return self.username
    