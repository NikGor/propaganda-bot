from rest_framework.exceptions import NotFound, ValidationError

from .analyze_model.analyze_news import analyze_news_with_chatgpt
from .models import LinkAnalysis
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .parser import (
    get_article_header,
    get_article_authors,
    get_article_publish_date,
    get_article_image, get_article_text,
)
from .serializers import AuthorsNotesUpdateSerializer, ImageNotesUpdateSerializer


def get_or_create_link_analysis(url):
    # Сначала проверяем, существует ли уже объект LinkAnalysis для данного URL.
    link_analysis, created = LinkAnalysis.objects.get_or_create(url=url)

    # Если объект был только что создан, то заполняем его данными.
    if created:
        link_analysis.article_header = get_article_header(url)
        link_analysis.article_text = get_article_text(url)
        link_analysis.article_authors = ', '.join(get_article_authors(url))
        publish_date = get_article_publish_date(url)
        if publish_date:
            link_analysis.article_publish_date = publish_date.date()
        link_analysis.article_image = get_article_image(url)
        link_analysis.analysis_result = analyze_news_with_chatgpt(link_analysis.article_text)
        link_analysis.save()

    return link_analysis


def article_swagger_decorator():
    parameters = [
        openapi.Parameter('url', openapi.IN_QUERY, description="URL of the article", type=openapi.TYPE_STRING)
    ]
    return swagger_auto_schema(manual_parameters=parameters)


def analyze_link_swagger_decorator():
    parameters = [
        openapi.Parameter('url', openapi.IN_QUERY, description="URL to analyze", type=openapi.TYPE_STRING)
    ]
    return swagger_auto_schema(manual_parameters=parameters)


def authors_notes_update_swagger_decorator():
    return swagger_auto_schema(
        request_body=AuthorsNotesUpdateSerializer,
        responses={200: 'Обновленные заметки автора успешно сохранены'},
        operation_description="Обновление заметок автора для анализа ссылки"
    )


def update_authors_notes(link_analysis_id, new_notes):
    link_analysis = LinkAnalysis.objects.get(pk=link_analysis_id)
    link_analysis.article_authors_community_notes = new_notes
    link_analysis.save()
    return link_analysis


def image_notes_update_swagger_decorator():
    return swagger_auto_schema(
        request_body=ImageNotesUpdateSerializer,
        responses={200: 'Обновленные заметки изображения успешно сохранены'},
        operation_description="Обновление заметок изображения для анализа ссылки"
    )


def update_image_notes(link_analysis_id, new_notes):
    link_analysis = LinkAnalysis.objects.get(pk=link_analysis_id)
    link_analysis.article_image_community_notes = new_notes
    link_analysis.save()
    return link_analysis


def get_id_by_url_swagger_decorator():
    return swagger_auto_schema(
        operation_description="Получение ID по URL",
        operation_summary="Получает ID записи LinkAnalysis по заданному URL",
        responses={
            200: openapi.Response(description="Успешно найден ID", examples={"application/json": {"id": "1"}}),
            400: "Неверный запрос или отсутствует параметр URL",
            404: "Запись не найдена"
        },
        manual_parameters=[
            openapi.Parameter("url", openapi.IN_QUERY,
                              description="URL анализируемой ссылки",
                              type=openapi.TYPE_STRING, required=True)
        ]
    )


def get_id_by_url(request):
    url = request.query_params.get('url', None)
    if not url:
        raise ValidationError({'url': 'This field is required.'})

    try:
        link_analysis = LinkAnalysis.objects.get(url=url)
        return link_analysis.id
    except LinkAnalysis.DoesNotExist:
        raise NotFound(detail="LinkAnalysis with given URL not found.")
