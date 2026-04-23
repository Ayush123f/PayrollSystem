from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extends Django's built-in User model with a role field.
    Already includes: username, password, first_name,
    last_name, email, is_active, is_staff, date_joined
    """
    ROLE_CHOICES = [
        ('admin',    'Admin'),
        ('hr',       'HR'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee'
    )

    def is_admin(self):
        return self.role == 'admin'

    def is_hr_or_admin(self):
        return self.role in ('admin', 'hr')

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"