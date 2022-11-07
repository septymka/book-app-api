from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from authors.serializers import AuthorSerializer
from authors.models import Author


AUTHORS_URL = reverse('author:author-list')


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
        self.author_joe = {
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
        create_author()
        create_author(
            first_name='Terry',
            last_name='Pratchett',
            date_of_birth=date(1948, 4, 28),
            date_of_death=date(2015, 3, 12),
            description='American author, writer, and philanthropist.'
        )
        resp = self.client.get(AUTHORS_URL)
        authors = Author.objects.all().order_by('last_name', 'first_name')
        serializer = AuthorSerializer(authors, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_post_genres_nonexistent(self):
        resp = self.client.post(AUTHORS_URL, self.author_joe)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        author = Author.objects.get(id=resp.data['id'])
        for k, v in self.author_joe.items():
            self.assertEqual(getattr(author, k), v)
