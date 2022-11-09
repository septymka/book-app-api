import factory
from factory.faker import faker
from .models import Author
from datetime import datetime

fake = faker.Faker()


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = fake.first_name()
    last_name = fake.last_name()
    date_of_birth = datetime.strptime(fake.date(), '%Y-%m-%d').date()
    description = fake.paragraph()
