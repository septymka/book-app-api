from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from genres.serializers import GenreSerializer
from genres.models import Genre


GENRES_URL = reverse('genre:genre-list')


def detail_url(genre_id):
    return reverse('genre:genre-detail', args=[genre_id])


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

    def test_post_genres_nonexistent(self):
        new_genre_name = 'Drama'
        payload = {'name': new_genre_name}
        resp = self.client.post(GENRES_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['name'], new_genre_name)

    def test_post_genres_existing(self):
        new_genre_name = 'History'
        Genre.objects.create(name=new_genre_name)
        payload = {'name': new_genre_name}
        resp = self.client.post(GENRES_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class DetailGenreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name='Fantasy')

    def test_get_genre_detail_existing(self):
        serializer = GenreSerializer(self.genre)
        url = detail_url(self.genre.id)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_get_genre_detail_nonexistent(self):
        nonexistent_genre_id = 100
        url = detail_url(nonexistent_genre_id)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_genre(self):
        url = detail_url(self.genre.id)
        payload = {'name': 'Mystery'}
        resp = self.client.patch(url, payload)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.genre.refresh_from_db()
        self.assertEqual(self.genre.name, payload['name'])

    def test_patch_genre_nonexistent(self):
        nonexistent_genre_id = 100
        url = detail_url(nonexistent_genre_id)
        payload = {'name': 'Mystery'}
        resp = self.client.patch(url, payload)

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_genre(self):
        url = detail_url(self.genre.id)
        resp = self.client.delete(url)

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Genre.objects.filter(id=self.genre.id).exists())

    def test_delete_genre_nonexistent(self):
        nonexistent_genre_id = 100
        url = detail_url(nonexistent_genre_id)
        resp = self.client.delete(url)

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
