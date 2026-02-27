from django.contrib import admin
from .models import Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'contact_email', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'short_name', 'contact_email')
    raw_id_fields = ('user',)
