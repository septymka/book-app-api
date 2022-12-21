from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from authors.models import Author
from authors.serializers import AuthorSerializer
from authors.permissions import IsAdminOrReadOnly


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow to view or modify genre.
    """
    queryset = Author.objects.all().order_by('last_name', 'first_name')
    serializer_class = AuthorSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAdminOrReadOnly]
