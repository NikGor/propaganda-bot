from django.db import models


class LinkAnalysis(models.Model):
    url = models.URLField(unique=True)
    article_header = models.CharField(max_length=255, blank=True)
    article_authors = models.CharField(max_length=255, blank=True)
    article_authors_community_notes = models.CharField(max_length=255, blank=True)
    article_publish_date = models.DateField(blank=True, null=True)
    article_image = models.URLField(blank=True)
    article_image_community_notes = models.URLField(blank=True)
    analysis_result = models.TextField(blank=True)

    def __str__(self):
        return self.url
