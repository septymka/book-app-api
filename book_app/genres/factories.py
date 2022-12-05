import factory

from genres.models import Genre


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = 'Fantasy'
