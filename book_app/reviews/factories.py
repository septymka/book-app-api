import factory
from factory.faker import faker

from .models import BookReview
from accounts.factories import UserFactory
from books.factories import BookFactory


fake = faker.Faker()


class BookReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookReview

    user = factory.SubFactory(UserFactory)
    book = factory.SubFactory(BookFactory)
    rating = fake.pyint(min_value=1, max_value=10)
    review = fake.text()
