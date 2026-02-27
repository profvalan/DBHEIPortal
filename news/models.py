from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from institutions.models import Institution


SDG_GOALS = [
    (1,  'SDG 1 - No Poverty'),
    (2,  'SDG 2 - Zero Hunger'),
    (3,  'SDG 3 - Good Health and Well-being'),
    (4,  'SDG 4 - Quality Education'),
    (5,  'SDG 5 - Gender Equality'),
    (6,  'SDG 6 - Clean Water and Sanitation'),
    (7,  'SDG 7 - Affordable and Clean Energy'),
    (8,  'SDG 8 - Decent Work and Economic Growth'),
    (9,  'SDG 9 - Industry, Innovation and Infrastructure'),
    (10, 'SDG 10 - Reduced Inequalities'),
    (11, 'SDG 11 - Sustainable Cities and Communities'),
    (12, 'SDG 12 - Responsible Consumption and Production'),
    (13, 'SDG 13 - Climate Action'),
    (14, 'SDG 14 - Life Below Water'),
    (15, 'SDG 15 - Life on Land'),
    (16, 'SDG 16 - Peace, Justice and Strong Institutions'),
    (17, 'SDG 17 - Partnerships for the Goals'),
]

SDG_COLORS = {
    1: '#E5243B', 2: '#DDA63A', 3: '#4C9F38', 4: '#C5192D', 5: '#FF3A21',
    6: '#26BDE2', 7: '#FCC30B', 8: '#A21942', 9: '#FD6925', 10: '#DD1367',
    11: '#FD9D24', 12: '#BF8B2E', 13: '#3F7E44', 14: '#0A97D9', 15: '#56C02B',
    16: '#00689D', 17: '#19486A',
}


class SDGGoal(models.Model):
    number = models.IntegerField(choices=SDG_GOALS, unique=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return dict(SDG_GOALS).get(self.number, f'SDG {self.number}')

    def get_color(self):
        return SDG_COLORS.get(self.number, '#333333')


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'News Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class NewsItem(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PENDING, 'Pending Approval'),
        (STATUS_APPROVED, 'Approved / Published'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='news_items')
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    summary = models.TextField(max_length=500, help_text='Brief summary (max 500 chars)')
    content = models.TextField()
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, blank=True)
    sdg_goals = models.ManyToManyField(SDGGoal, blank=True, related_name='news_items')
    video_url = models.URLField(blank=True, help_text='YouTube / Vimeo URL')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    featured_image = models.ImageField(upload_to='news_images/%Y/%m/', blank=True, null=True)
    admin_notes = models.TextField(blank=True, help_text='Admin feedback on approval/rejection')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            n = 1
            while NewsItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})

    def get_embed_url(self):
        """Convert YouTube/Vimeo URL to embed URL."""
        url = self.video_url
        if not url:
            return None
        if 'youtube.com/watch' in url:
            video_id = url.split('v=')[-1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        if 'vimeo.com/' in url:
            video_id = url.split('vimeo.com/')[-1].split('?')[0]
            return f"https://player.vimeo.com/video/{video_id}"
        return url


class NewsImage(models.Model):
    news_item = models.ForeignKey(NewsItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news_gallery/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.news_item.title}"
