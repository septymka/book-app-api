from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reviews import views


router = DefaultRouter()
router.register('reviews', views.BookReviewViewSet)

app_name = 'review'
base_name = 'review'

urlpatterns = [
    path('', include(router.urls)),
]
