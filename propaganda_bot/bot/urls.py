from django.urls import path
from .views import (AnalyzeLinkView, ArticleHeaderView,
                    ArticleTextView, ArticleAuthorsView,
                    ArticlePublishDateView, ArticleImageView,
                    ArticleSummaryView, AuthorsNotesUpdateView,
                    ImageNotesUpdateView, GetIDByURLView, )

urlpatterns = [
    path('get_header/', ArticleHeaderView.as_view(), name='article-header'),
    path('get_text/', ArticleTextView.as_view(), name='article-text'),
    path('get_authors/', ArticleAuthorsView.as_view(), name='article-authors'),
    path('get_publish_date/', ArticlePublishDateView.as_view(), name='article-publish-date'),
    path('get_image/', ArticleImageView.as_view(), name='article-image'),
    path('get_summary/', ArticleSummaryView.as_view(), name='article-summary'),
    path('analyze/', AnalyzeLinkView.as_view(), name='analyze_link'),
    path('update_authors_notes/<int:pk>/', AuthorsNotesUpdateView.as_view(), name='update-authors-notes'),
    path('update_image_notes/<int:pk>/', ImageNotesUpdateView.as_view(), name='update-image-notes'),
    path('get-id-by-url/', GetIDByURLView.as_view(), name='get-id-by-url'),
]
