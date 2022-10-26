from django.urls import path, include
from rest_framework.routers import DefaultRouter

from genres import views


router = DefaultRouter()
router.register('genres', views.GenreViewSet)

app_name = 'genre'

urlpatterns = [
    path('', include(router.urls)),
]
