from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from authors.factories import AuthorFactory
from books.factories import BookFactory
from books.models import Book
from books.serializers import BookSerializer
from accounts.models import User


BOOKS_URL = reverse('book:book-list')

def detail_url(book_id):
    return reverse('book:book-detail', args=[book_id])


class PublicBookApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = AuthorFactory()
        self.payload = {
            'title': 'My Book',
            'summary': 'The Book',
            'authors': [self.author.id],
            'genres': [
                {
                    'name': 'Fantasy'
                }
            ]
        }

    def test_get_books_with_no_books(self):
        resp = self.client.get(BOOKS_URL)
        expected = []
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, expected)

    def test_get_books(self):
        BookFactory()
        BookFactory()
        resp = self.client.get(BOOKS_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_get_book_detail_existing(self):
        book = BookFactory()
        serializer = BookSerializer(book)
        url = detail_url(book.id)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)


    def test_get_book_detail_nonexistent(self):
        nonexistent_book_id = 100
        url = detail_url(nonexistent_book_id)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def test_post_book_admin_required(self):
        resp = self.client.post(BOOKS_URL, self.payload)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_book_admin_required(self):
        book = BookFactory()
        url = detail_url(book.id)
        resp = self.client.patch(url, self.payload)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_admin_required(self):
        book = BookFactory()
        url = detail_url(book.id)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminBookApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(
            'admin@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.superuser)
        self.nonexistent_book_id = 100
        self.author = AuthorFactory()
        self.payload = {
            'title': 'My Book',
            'summary': 'The Book',
            'authors': [self.author.id],
            'genres': [
                {
                    'name': 'Fantasy'
                }
            ]
        }

    def test_post_book(self):
        resp = self.client.post(BOOKS_URL, self.payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=resp.data['id'])
        for k, v in self.payload.items():
            if k == 'authors':
                self.assertEqual(v, [self.author.id])
            elif k == 'genres':
                self.assertEqual(v, [{'name': 'Fantasy'}])

            else:
                self.assertEqual(getattr(book, k), v)

    def test_patch_book(self):
        book = BookFactory()
        url = detail_url(book.id)
        payload = {
            'title': 'The Book!'
        }
        resp = self.client.patch(url, payload)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['title'], payload['title'])

    def test_patch_book_nonexistent(self):
        url = detail_url(self.nonexistent_book_id)
        resp = self.client.patch(url, self.payload)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_book(self):
        book = BookFactory()
        url = detail_url(book.id)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())

    def test_delete_author_nonexistent(self):
        url = detail_url(self.nonexistent_book_id)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
