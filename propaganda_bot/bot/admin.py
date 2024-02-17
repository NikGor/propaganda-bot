from django.contrib import admin
from .models import LinkAnalysis


@admin.register(LinkAnalysis)
class LinkAnalysisAdmin(admin.ModelAdmin):
    list_display = ('url', 'article_header', 'article_authors', 'article_publish_date', 'article_image')
    search_fields = ('url', 'article_header', 'article_authors')
    list_filter = ('article_publish_date',)
    date_hierarchy = 'article_publish_date'
    fields = ('url', 'article_header', 'article_authors',
              'article_authors_community_notes', 'article_publish_date',
              'article_image', 'article_image_community_notes',
              'analysis_result')
    readonly_fields = ('analysis_result',)
