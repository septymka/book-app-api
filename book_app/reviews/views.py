from rest_framework import viewsets, status
from rest_framework.response import Response


from reviews.models import BookReview
from reviews.serializers import BookReviewSerializer


class BookReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow to view and modify book review
    """
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            super().create()
        else:
            data = {'message': 'Authentication required'}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
