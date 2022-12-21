from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from books.models import Book
from books.serializers import BookSerializer
from books.permissions import IsAdminOrReadOnly

from authors.models import Author


class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAdminOrReadOnly]


    def perform_create(self, serializer):
        authors_id = self.request.data.get("authors")
        authors = []
        for author_id in authors_id:
            authors.append(Author.objects.filter(id=author_id).first())

        try:
            serializer.save(authors=authors)
        except Exception as e:
            print(e)
