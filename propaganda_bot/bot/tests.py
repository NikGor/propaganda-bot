from django.test import TestCase
from django.urls import reverse
from .models import LinkAnalysis
from rest_framework.test import APITestCase
from rest_framework import status


class LinkAnalysisTests(TestCase):

    # def test_analysis_creation_and_retrieval(self):
    #     url = "https://example.com"
    #     response = self.client.get(reverse('analyze_link') + f'?url={url}')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("Result of analysis", response.json()['analysis_result'])
    #
    #     # Проверяем, сохранена ли ссылка в базе данных
    #     self.assertTrue(LinkAnalysis.objects.filter(url=url).exists())

    def test_analysis_retrieval_existing_link(self):
        url = "https://example.com"
        LinkAnalysis.objects.create(url=url, analysis_result="Existing analysis result")

        response = self.client.get(reverse('analyze_link') + f'?url={url}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Existing analysis result", response.json()['analysis_result'])


class AuthorsNotesUpdateViewTest(APITestCase):
    def setUp(self):
        # Создание тестового объекта LinkAnalysis
        self.link_analysis = LinkAnalysis.objects.create(
            article_authors_community_notes="Initial notes"
        )
        self.url = reverse('update-authors-notes', kwargs={'pk': self.link_analysis.pk})

    def test_update_authors_notes(self):
        # Правильно структурированные данные для обновления
        new_notes = {"article_authors_community_notes": "Updated notes"}
        # Использование format='json' для автоматической сериализации данных
        response = self.client.patch(self.url, new_notes, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.link_analysis.refresh_from_db()
        # Проверка обновления данных
        self.assertEqual(self.link_analysis.article_authors_community_notes,
                         new_notes['article_authors_community_notes'])


class GetIDByURLViewTest(APITestCase):
    def setUp(self):
        # Создаем тестовую запись в базе данных
        self.test_url = 'http://example.com'
        self.link_analysis = LinkAnalysis.objects.create(url=self.test_url,
                                                         article_authors_community_notes='Test notes')
        self.get_id_by_url_path = reverse('get-id-by-url')

    def test_get_id_by_existing_url(self):
        # Тест на успешное получение ID по существующему URL
        response = self.client.get(self.get_id_by_url_path, {'url': self.test_url})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.link_analysis.id)

    def test_get_id_by_non_existing_url(self):
        # Тест на получение ошибки при запросе несуществующего URL
        non_existing_url = 'http://nonexisting.com'
        response = self.client.get(self.get_id_by_url_path, {'url': non_existing_url})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_id_without_url(self):
        # Тест на обработку запроса без URL
        response = self.client.get(self.get_id_by_url_path)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
