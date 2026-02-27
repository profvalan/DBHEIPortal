from django.contrib import admin
from .models import Institution, InstitutionStats


class InstitutionStatsInline(admin.StackedInline):
    model = InstitutionStats
    extra = 0


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'place', 'foundation_year', 'institution_category', 'institution_type', 'is_active')
    list_filter = ('province', 'institution_category', 'institution_type', 'is_active')
    search_fields = ('name', 'short_name', 'place', 'province')
    raw_id_fields = ('user',)
    inlines = [InstitutionStatsInline]


@admin.register(InstitutionStats)
class InstitutionStatsAdmin(admin.ModelAdmin):
    list_display = ('institution', 'total_students', 'total_faculty', 'total_programs', 'research_papers', 'updated_at')
    search_fields = ('institution__name',)
    raw_id_fields = ('institution',)
