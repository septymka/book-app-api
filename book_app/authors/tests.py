from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from authors.serializers import AuthorSerializer
from authors.models import Author
from authors.factories import AuthorFactory
from accounts.models import User



AUTHORS_URL = reverse('author:author-list')


def detail_url(author_id):
    return reverse('author:author-detail', args=[author_id])


class PublicAuthorApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'first_name': 'Joe',
            'last_name': 'Simpson',
            'date_of_birth': date(1960, 8, 13),
            'description': 'British mountaineer and author.'
        }

    def test_get_authors_with_no_authors(self):
        resp = self.client.get(AUTHORS_URL)
        expected = []
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), expected)

    def test_get_authors_with_two_authors(self):
        AuthorFactory()
        AuthorFactory()
        resp = self.client.get(AUTHORS_URL)
        authors = Author.objects.all().order_by('last_name', 'first_name')
        serializer = AuthorSerializer(authors, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_get_author_detail_existing(self):
        author = AuthorFactory()
        serializer = AuthorSerializer(author)
        url = detail_url(author.id)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_get_author_detail_nonexistent(self):
        nonexistent_author_id = 100
        url = detail_url(nonexistent_author_id)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_author_auth_admin_required(self):
        resp = self.client.post(AUTHORS_URL, self.payload)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_author_auth_admin_required(self):
        author = AuthorFactory()
        resp = self.client.patch(detail_url(author.id), self.payload)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_author_auth_admin_required(self):
        author = AuthorFactory()
        resp = self.client.delete(detail_url(author.id), self.payload)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminAythorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser('admin@example.com', 'testpass123')
        self.client.force_authenticate(self.superuser)
        self.payload = {
            'first_name': 'Joe',
            'last_name': 'Simpson',
            'date_of_birth': date(1960, 8, 13),
            'description': 'British mountaineer and author.'
        }
        self.nonexistent_author_id = 100

    def test_post_author(self):
        resp = self.client.post(AUTHORS_URL, self.payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        author = Author.objects.get(id=resp.data['id'])
        for k, v in self.payload.items():
            self.assertEqual(getattr(author, k), v)

    def test_patch_author(self):
        author = AuthorFactory()
        url = detail_url(author.id)
        resp = self.client.patch(url, self.payload)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['first_name'], self.payload['first_name'])

    def test_patch_author_nonexistent(self):
        url = detail_url(self.nonexistent_author_id)
        resp = self.client.patch(url, self.payload)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_author(self):
        author = AuthorFactory()
        url = detail_url(author.id)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=author.id).exists())

    def test_delete_author_nonexistent(self):
        url = detail_url(self.nonexistent_author_id)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
