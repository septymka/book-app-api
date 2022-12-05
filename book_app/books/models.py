from django.db import models

from genres.models import Genre
from authors.models import Author


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author)
    summary = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField(Genre)
    image = models.CharField(max_length=500, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    number_of_ratings = models.IntegerField(default=0)

    def __str__(self):
        return self.title
