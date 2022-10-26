from rest_framework import serializers
from genres.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
        read_only_fields = ['id']
