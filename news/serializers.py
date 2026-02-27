from rest_framework import serializers
from .models import NewsItem, SDGGoal, NewsCategory, NewsImage
from institutions.models import Institution


class SDGGoalSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = SDGGoal
        fields = ['number', 'label', 'color']

    def get_label(self, obj):
        return str(obj)

    def get_color(self, obj):
        return obj.get_color()


class InstitutionBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'short_name', 'website']


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image', 'caption']


class NewsItemSerializer(serializers.ModelSerializer):
    institution = InstitutionBriefSerializer(read_only=True)
    sdg_goals = SDGGoalSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = NewsImageSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()
    embed_url = serializers.SerializerMethodField()

    class Meta:
        model = NewsItem
        fields = [
            'id', 'title', 'slug', 'summary', 'content',
            'institution', 'category_name', 'sdg_goals',
            'featured_image', 'images', 'video_url', 'embed_url',
            'published_at', 'url',
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.get_absolute_url())
        return obj.get_absolute_url()

    def get_embed_url(self, obj):
        return obj.get_embed_url()
