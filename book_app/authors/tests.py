from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from authors.serializers import AuthorSerializer
from authors.models import Author


AUTHORS_URL = reverse('author:author-list')

def detail_url(author_id):
    return reverse('author:author-detail', args=[author_id])
def create_author(**params):
    defaults = {
        'first_name': 'Ken',
        'last_name': 'Follett',
        'date_of_birth': date(1949, 6, 5),
        'description': 'British author of thrillers and historical novels'
    }
    defaults.update(params)
    author = Author.objects.create(**defaults)
    return author


class AuthorApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_authors_with_no_authors(self):
        resp = self.client.get(AUTHORS_URL)
        expected = []
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), expected)

    def test_get_authors_with_two_authors(self):
        create_author()
        create_author(
            first_name='Terry',
            last_name='Pratchett',
            date_of_birth=date(1948, 4, 28),
            date_of_death=date(2015, 3, 12),
            description='English satirist and author of fantasy novels.'
        )
        resp = self.client.get(AUTHORS_URL)
        authors = Author.objects.all().order_by('last_name', 'first_name')
        serializer = AuthorSerializer(authors, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_post_genres(self):
        new_author = {
            'first_name': 'Joe',
            'last_name': 'Simpson',
            'date_of_birth': date(1960, 8, 13),
            'description': 'British mountaineer and author.'
        }
        resp = self.client.post(AUTHORS_URL, new_author)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        author = Author.objects.get(id=resp.data['id'])
        for k, v in new_author.items():
            self.assertEqual(getattr(author, k), v)


class DetailAuthorApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = create_author()
        self.nonexistent_author_id = 100
        self.payload = {
            'first_name': 'Kenneth'
        }

    def test_get_author_detail_existing(self):
        serializer = AuthorSerializer(self.author)
        url = detail_url(self.author.id)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)


    def test_get_author_detail_nonexistent(self):
        url = detail_url(self.nonexistent_author_id)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_author(self):
        url = detail_url(self.author.id)
        payload = {
            'first_name': 'Kenneth'
        }
        resp = self.client.patch(url, payload)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['first_name'], payload['first_name'])

    def test_patch_author_nonexistent(self):
        url = detail_url(self.nonexistent_author_id)
        resp = self.client.patch(url, self.payload)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_author(self):
        url = detail_url(self.author.id)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=self.author.id).exists())

    def test_delete_author_nonexistent(self):
        url = detail_url(self.nonexistent_author_id)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
