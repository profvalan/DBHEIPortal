from django.db import models
from django.urls import reverse
from accounts.models import User


INSTITUTION_CATEGORY_CHOICES = [
    ('affiliated', 'Affiliated Institute'),
    ('autonomous', 'Autonomous Institute'),
    ('university', 'University (Degree Granting)'),
    ('technical', 'Technical/Poly Techniques'),
]

INSTITUTION_TYPE_CHOICES = [
    ('college', 'College'),
    ('university', 'University'),
]

PROVINCE_CHOICES = [
    ('Bengaluru', 'Bengaluru'),
    ('Chennai', 'Chennai'),
    ('Dimapur', 'Dimapur'),
    ('Guwahati', 'Guwahati'),
    ('Hyderabad', 'Hyderabad'),
    ('Kolkatta', 'Kolkatta'),
    ('Mumbai', 'Mumbai'),
    ('New Delhi', 'New Delhi'),
    ('Panjim', 'Panjim'),
    ('Shillong', 'Shillong'),
    ('Tiruchy', 'Tiruchy'),
]


class Institution(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='institution')
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, blank=True)
    logo = models.ImageField(upload_to='institution_logos/', blank=True, null=True)
    website = models.URLField(blank=True)
    place = models.CharField(max_length=150, blank=True)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, blank=True)
    foundation_year = models.PositiveIntegerField(null=True, blank=True)
    institution_category = models.CharField(
        max_length=30, choices=INSTITUTION_CATEGORY_CHOICES, blank=True
    )
    institution_type = models.CharField(
        max_length=30, choices=INSTITUTION_TYPE_CHOICES, blank=True
    )
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

    def get_absolute_url(self):
        return reverse('institutions:detail', kwargs={'pk': self.pk})


class InstitutionStats(models.Model):
    """Editable statistics for each institution - one row per institution."""
    institution = models.OneToOneField(Institution, on_delete=models.CASCADE, related_name='stats')
    total_students = models.PositiveIntegerField(default=0, verbose_name='Total Students')
    total_faculty = models.PositiveIntegerField(default=0, verbose_name='Total Faculty')
    total_programs = models.PositiveIntegerField(default=0, verbose_name='Programs Offered')
    total_departments = models.PositiveIntegerField(default=0, verbose_name='Departments')
    phd_holders = models.PositiveIntegerField(default=0, verbose_name='PhD Holders')
    research_papers = models.PositiveIntegerField(default=0, verbose_name='Research Papers Published')
    naac_grade = models.CharField(max_length=10, blank=True, verbose_name='NAAC Grade')
    campus_area_acres = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, verbose_name='Campus Area (acres)'
    )
    placement_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, verbose_name='Placement Rate (%)'
    )
    library_books = models.PositiveIntegerField(default=0, verbose_name='Library Books')
    hostels = models.PositiveIntegerField(default=0, verbose_name='Hostels')
    labs = models.PositiveIntegerField(default=0, verbose_name='Laboratories')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Institution Statistics'
        verbose_name_plural = 'Institution Statistics'

    def __str__(self):
        return f"Stats for {self.institution.name}"
