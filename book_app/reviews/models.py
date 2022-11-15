from django.db import models

from books.models import Book
from accounts.models import User


class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.book
