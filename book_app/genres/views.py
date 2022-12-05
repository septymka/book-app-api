from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from genres.models import Genre
from genres.serializers import GenreSerializer
from genres.permissions import IsAdminOrReadOnly


class GenreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view or modify genres.
    """
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
