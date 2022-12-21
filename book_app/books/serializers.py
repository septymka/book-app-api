from rest_framework import serializers

from books.models import Book
from authors.serializers import AuthorInBookSerializer
from genres.serializers import GenreSerializer
from genres.models import Genre


class BookSerializer(serializers.ModelSerializer):

    authors = AuthorInBookSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'authors',
            'summary',
            'genres',
            'image',
            'rating',
            'number_of_ratings'
        ]

        read_only_fields = ['id']

    def create(self, validated_data):
        print(validated_data)
        genres = validated_data.pop('genres', [])
        authors = validated_data.pop('authors', [])
        book = Book.objects.create(**validated_data)
        book.authors.set(authors)
        for genre in genres:
            genre_obj, created = Genre.objects.get_or_create(**genre)
            book.genres.add(genre_obj)

        return book




class BookInReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'authors'
        ]
        read_only_fields = ['id']
