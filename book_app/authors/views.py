from rest_framework import viewsets

from authors.models import Author
from authors.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow to view or modify genre.
    """
    queryset = Author.objects.all().order_by('last_name', 'first_name')
    serializer_class = AuthorSerializer
