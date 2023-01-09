from django.db import models
from django.db.models import Avg

from genres.models import Genre
from authors.models import Author
#from reviews.models import BookReview


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='authors')
    summary = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField(Genre)
    image = models.CharField(max_length=500, blank=True, null=True)


    @property
    def rating(self):
        avg = None
        reviews = self.bookreview_set.all()
        if reviews:
            ratings = [review.rating for review in reviews]
            avg = sum(ratings)/len(ratings)
        return avg

    @property
    def number_of_ratings(self):
        reviews = self.bookreview_set.all()
        num_of_ratings = 0
        if reviews:
            num_of_ratings = reviews.count()
        return num_of_ratings

    def __str__(self):
        return self.title
