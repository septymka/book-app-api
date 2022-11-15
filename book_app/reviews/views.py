from rest_framework import viewsets

from reviews.models import BookReview
from reviews.serializers import BookReviewSerializer


class BookReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow to view and modify book review
    """
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
