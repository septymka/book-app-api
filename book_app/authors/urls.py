from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authors import views


router = DefaultRouter()
router.register('authors', views.AuthorViewSet)

app_name = 'author'

urlpatterns = [
    path('', include(router.urls))
]
