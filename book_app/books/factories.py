import factory
from factory.faker import faker
from .models import Book

fake = faker.Faker()


class BookFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Book

    title = fake.text(max_nb_chars=20)
