from rest_framework import serializers
from propaganda_bot.bot.models import LinkAnalysis


class LinkAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkAnalysis
        fields = [
            'url', 'article_header', 'article_authors', 'article_authors_community_notes',
            'article_publish_date', 'article_image', 'article_image_community_notes',
            'analysis_result',
        ]


class ArticleSerializer(serializers.Serializer):
    url = serializers.URLField()


class AuthorsNotesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkAnalysis
        fields = ['article_authors_community_notes']


class ImageNotesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkAnalysis
        fields = ['article_image_community_notes']


class URLSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
