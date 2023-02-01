import factory
from factory.faker import faker
from books.models import Book
from authors.factories import AuthorFactory
from genres.factories import GenreFactory

fake = faker.Faker()


class BookFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Book

    title = fake.text(max_nb_chars=20)
    summary = fake.text(max_nb_chars=100)
    image = fake.image_url()
    genres = factory.SubFactory(GenreFactory)

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        author = AuthorFactory()
        self.authors.add(author)


    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        genre = GenreFactory()
        self.genres.add(genre)
