from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from books.factories import BookFactory
from reviews.models import BookReview
from reviews.factories import BookReviewFactory
from reviews.serializers import BookReviewSerializer
from accounts.factories import UserFactory


REVIEW_URL = reverse('review:bookreview-list')


def detail_url(review_id):
    return reverse('review:bookreview-detail', args=[review_id])


class PublicReviewApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.review = BookReviewFactory()
        self.payload = {
            "book": 1,
            "rating": 7,
            "review": "Good"
        }

    def test_get_all_reviews(self):
        BookReviewFactory()
        reviews = BookReview.objects.all()
        serializer = BookReviewSerializer(reviews, many=True)
        resp = self.client.get(REVIEW_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_get_review(self):
        review_id = self.review.id
        resp = self.client.get(detail_url(review_id))
        serializer = BookReviewSerializer(self.review)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_create_auth_required(self):
        resp = self.client.post(REVIEW_URL, data=self.payload)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReviewApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.book = BookFactory()
        self.user = UserFactory()
        self.payload = {
            "book": self.book.id,
            "rating": 7,
            "review": "Good"
        }
        self.client.force_authenticate(self.user)

    def test_create_review(self):
        resp = self.client.post(REVIEW_URL, data=self.payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        review = BookReview.objects.get(id=resp.data['id'])
        self.assertEqual(review.user, self.user)

    def test_update_review(self):
        review = BookReviewFactory(
            user=self.user,
            book=self.book,
            rating=8,
            review="New review"
        )
        resp = self.client.patch(detail_url(review.id), data=self.payload)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.review, self.payload["review"])
        self.assertEqual(review.rating, self.payload["rating"])

    def test_update_other_user_review_error(self):
        other_user = UserFactory()
        review = BookReviewFactory(user=other_user)
        resp = self.client.patch(detail_url(review.id), data=self.payload)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review(self):
        review = BookReviewFactory(user=self.user)
        resp = self.client.delete(detail_url(review.id))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_user_review_error(self):
        other_user = UserFactory()
        review = BookReviewFactory(user=other_user)
        resp = self.client.delete(detail_url(review.id))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
