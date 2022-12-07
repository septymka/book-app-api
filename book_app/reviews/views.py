from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from reviews.permissions import IsOwnerOrReadOnly
from reviews.models import BookReview
from reviews.serializers import BookReviewSerializer


class BookReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow to view and modify book review
    """
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
