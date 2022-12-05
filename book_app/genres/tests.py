from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from genres.serializers import GenreSerializer
from genres.models import Genre
from genres.factories import GenreFactory
from accounts.models import User


GENRES_URL = reverse('genre:genre-list')


def detail_url(genre_id):
    return reverse('genre:genre-detail', args=[genre_id])


class PublicGenreApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.payload = {'name': 'History'}

    def test_get_genres_with_no_genres(self):
        resp = self.client.get(GENRES_URL)
        expected = []
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), expected)

    def test_get_all_genres(self):
        GenreFactory()
        GenreFactory(name='Crime')

        resp = self.client.get(GENRES_URL)

        genres = Genre.objects.all().order_by('name')
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_get_genre_detail_existing(self):
        genre = GenreFactory()
        serializer = GenreSerializer(genre)
        url = detail_url(genre.id)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_get_genre_detail_nonexistent(self):
        nonexistent_genre_id = 100
        url = detail_url(nonexistent_genre_id)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_genre_auth_admin_required(self):
        resp = self.client.post(GENRES_URL, self.payload)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_genre_auth_admin_required(self):
        genre = GenreFactory()
        resp = self.client.patch(detail_url(genre.id), self.payload)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_genre_auth_admin_required(self):
        genre = GenreFactory()
        resp = self.client.delete(detail_url(genre.id))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminGenreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser('admin@example.com', 'testpass123')
        self.client.force_authenticate(self.superuser)
        self.payload = {'name': 'Mystery'}
        self.nonexistent_genre_id = 100


    def test_post_genre(self):
        resp = self.client.post(GENRES_URL, data=self.payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_post_genre_existing(self):
        GenreFactory(name=self.payload['name'])
        resp = self.client.post(GENRES_URL, data=self.payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_genre(self):
        genre = GenreFactory()
        resp = self.client.patch(detail_url(genre.id), self.payload)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], self.payload['name'])

    def test_patch_genre_nonexistent(self):
        resp = self.client.patch(detail_url(self.nonexistent_genre_id), self.payload)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_genre(self):
        genre = GenreFactory()
        resp = self.client.delete(detail_url(genre.id))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_genre_nonexistent(self):
        genre = GenreFactory()
        resp = self.client.delete(detail_url(self.nonexistent_genre_id))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
