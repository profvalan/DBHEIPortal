from django.db import models
from accounts.models import User


class Institution(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='institution')
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, blank=True)
    logo = models.ImageField(upload_to='institution_logos/', blank=True, null=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
