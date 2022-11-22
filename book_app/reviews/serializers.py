from rest_framework import serializers
from reviews.models import BookReview


class BookReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )


    class Meta:
        model = BookReview
        fields = [
            'id',
            'user',
            'book',
            'rating',
            'review'
        ]
        read_only_fields = ['id']
