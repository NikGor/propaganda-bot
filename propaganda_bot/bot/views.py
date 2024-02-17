from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from .services import (get_or_create_link_analysis, analyze_link_swagger_decorator,
                       article_swagger_decorator, update_authors_notes, update_image_notes, get_id_by_url,
                       authors_notes_update_swagger_decorator, image_notes_update_swagger_decorator,
                       get_id_by_url_swagger_decorator,
                       )
from .serializers import (LinkAnalysisSerializer, AuthorsNotesUpdateSerializer,
                          ImageNotesUpdateSerializer)
from .parser import (
    get_article_header,
    get_article_text,
    get_article_authors,
    get_article_publish_date,
    get_article_image,
    get_article_summary
)


class ArticleHeaderView(APIView):
    @article_swagger_decorator()
    def get(self, request, *args, **kwargs):
        url = request.query_params.get('url')
        if not url:
            return Response({'error': 'URL parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)
        header = get_article_header(url)
        return Response({'header': header})


class ArticleTextView(APIView):
    @article_swagger_decorator()
    def get(self, request, *args, **kwargs):
        url = request.query_params.get('url')
        if not url:
            return Response({'error': 'URL parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)
        text = get_article_text(url)
        return Response({'text': text})


class ArticleAuthorsView(APIView):
    @article_swagger_decorator()
    def get(self, request, *args, **kwargs):
        url = request.query_params.get('url')
        if not url:
            return Response({'error': 'URL parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)
        authors = get_article_authors(url)
        return Response({'authors': authors})


class ArticlePublishDateView(APIView):
    @article_swagger_decorator()
    def get(self, request, *args, **kwargs):
        url = request.query_params.get('url')
        if not url:
            return Response({'error': 'URL parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)
        publish_date = get_article_publish_date(url)
        return Response({'publish_date': publish_date})


class ArticleImageView(APIView):
    @article_swagger_decorator()
    def get(self, request, *args, **kwargs):
        url = request.query_params.get('url')
        if not url:
            return Response({'error': 'URL parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)
        image = get_article_image(url)
        return Response({'image': image})


class ArticleSummaryView(APIView):
    @article_swagger_decorator()
    def get(self, request, *args, **kwargs):
        url = request.query_params.get('url')
        if not url:
            return Response({'error': 'URL parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)
        summary = get_article_summary(url)
        return Response({'summary': summary})


class AnalyzeLinkView(APIView):

    @analyze_link_swagger_decorator()
    def get(self, request, *args, **kwargs):
        url = request.query_params.get('url')
        if not url:
            return Response({'error': 'URL parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)

        link_analysis = get_or_create_link_analysis(url)
        serializer = LinkAnalysisSerializer(link_analysis)
        return Response(serializer.data)


class AuthorsNotesUpdateView(APIView):

    @authors_notes_update_swagger_decorator()
    def patch(self, request, pk):
        serializer = AuthorsNotesUpdateSerializer(data=request.data)
        if serializer.is_valid():
            updated_link_analysis = update_authors_notes(pk,
                                                         serializer.validated_data['article_authors_community_notes'])
            return Response(AuthorsNotesUpdateSerializer(updated_link_analysis).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageNotesUpdateView(APIView):

    @image_notes_update_swagger_decorator()
    def patch(self, request, pk):
        serializer = ImageNotesUpdateSerializer(data=request.data)
        if serializer.is_valid():
            updated_link_analysis = update_image_notes(pk, serializer.validated_data['article_image_community_notes'])
            return Response(ImageNotesUpdateSerializer(updated_link_analysis).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetIDByURLView(APIView):
    @get_id_by_url_swagger_decorator()
    def get(self, request, *args, **kwargs):
        try:
            link_id = get_id_by_url(request)
            return Response({'id': link_id}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({'detail': str(e.detail)}, status=status.HTTP_404_NOT_FOUND)
