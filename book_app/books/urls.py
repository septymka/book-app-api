from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books import views


router = DefaultRouter()
router.register('books', views.BookViewSet)

app_name = 'book'


urlpatterns = [
    path('', include(router.urls))
]
