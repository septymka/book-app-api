from rest_framework import serializers
from authors.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'last_name',
            'first_name',
            'date_of_birth',
            'date_of_death',
            'description'
        ]
        read_only_fields = ['id']
