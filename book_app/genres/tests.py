from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from genres.serializers import GenreSerializer
from genres.models import Genre


GENRES_URL = reverse('genre:genre-list')


class GenreApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_genres_with_no_genres(self):
        resp = self.client.get(GENRES_URL)
        expected = []
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), expected)

    def test_get_genres_with_two_genres(self):
        Genre.objects.create(name='Drama')
        Genre.objects.create(name='Crime')

        resp = self.client.get(GENRES_URL)

        genres = Genre.objects.all().order_by('name')
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_post_genre_nonexistent(self):
        new_genre_name = 'Drama'
        payload = {'name': new_genre_name}
        resp = self.client.post(GENRES_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['name'], new_genre_name)

    def test_post_genre_existing(self):
        new_genre_name = 'History'
        Genre.objects.create(name=new_genre_name)
        payload = {'name': new_genre_name}
        resp = self.client.post(GENRES_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
