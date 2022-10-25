from django.db import models

from books.models import Book


class BookReview(models.Model):
    # TODO add user
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.book
