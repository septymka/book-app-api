from rest_framework import serializers
from genres.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, validated_data):
        genre_obj, created = Genre.objects.get_or_create(**validated_data)
        return genre_obj

    def validate_name(self, value):
        return value.title()
