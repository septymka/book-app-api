from rest_framework import serializers
from reviews.models import BookReview


class BookReviewSerializer(serializers.ModelSerializer):

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

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        review = BookReview.objects.create(**validated_data)
        return review
