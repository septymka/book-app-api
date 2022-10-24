from rest_framework import viewsets

from genres.models import Genre
from genres.serializers import GenreSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view or modify genres.
    """
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
