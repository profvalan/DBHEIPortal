from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_INSTITUTION = 'institution'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_INSTITUTION, 'Institution'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_INSTITUTION)
    email = models.EmailField(unique=True)

    def is_admin_user(self):
        return self.role == self.ROLE_ADMIN

    def is_institution_user(self):
        return self.role == self.ROLE_INSTITUTION

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
