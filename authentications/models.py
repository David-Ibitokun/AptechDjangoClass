from django.contrib.auth.models import AbstractUser
from django.db import models

class UsersRegistration(AbstractUser):
    ACCOUNT_CHOICES = (
        ('user', 'User'),
        ('vendor', 'Vendor'),
    )
    
    account_type = models.CharField(max_length=20, choices=ACCOUNT_CHOICES, default='user')
    agreed_to_terms = models.BooleanField(default=False)