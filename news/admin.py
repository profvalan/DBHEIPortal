from django.contrib import admin
from django.utils import timezone
from .models import SDGGoal, NewsCategory, NewsItem, NewsImage


@admin.register(SDGGoal)
class SDGGoalAdmin(admin.ModelAdmin):
    list_display = ('number', '__str__')


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution', 'status', 'category', 'created_at', 'published_at')
    list_filter = ('status', 'category', 'institution', 'sdg_goals')
    search_fields = ('title', 'content', 'institution__name')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('sdg_goals',)
    readonly_fields = ('created_at', 'updated_at', 'submitted_at', 'published_at')
    inlines = [NewsImageInline]
    actions = ['approve_news', 'reject_news']

    def approve_news(self, request, queryset):
        updated = queryset.filter(status=NewsItem.STATUS_PENDING).update(
            status=NewsItem.STATUS_APPROVED,
            published_at=timezone.now()
        )
        self.message_user(request, f"{updated} news item(s) approved and published.")
    approve_news.short_description = "Approve selected news items"

    def reject_news(self, request, queryset):
        updated = queryset.filter(status=NewsItem.STATUS_PENDING).update(
            status=NewsItem.STATUS_REJECTED
        )
        self.message_user(request, f"{updated} news item(s) rejected.")
    reject_news.short_description = "Reject selected news items"
