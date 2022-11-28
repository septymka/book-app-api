import factory
from django.contrib.auth import get_user_model


DEFAULT_PASSWORD = 'test123'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: 'user%d@example.com' % n)
    first_name = 'John'
    last_name = 'Snow'
    password = factory.PostGenerationMethodCall(
        'set_password', DEFAULT_PASSWORD
    )
