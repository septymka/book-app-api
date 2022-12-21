from rest_framework import serializers

from reviews.models import BookReview
from accounts.serializers import UserSerializer
from books.serializers import BookInReviewSerializer
from books.models import Book


class BookReviewSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    book = BookInReviewSerializer(read_only=True)

    class Meta:
        model = BookReview
        fields = [
            'id',
            'user',
            'book',
            'rating',
            'review'
        ]

        read_only_fields = ['id', 'user']
