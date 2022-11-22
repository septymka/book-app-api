import factory
from django.contrib.auth import get_user_model


DEFAULT_PASSWORD = 'test123'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        # exclude = ('plaintext_password', )

    email = 'john_snow101@example.com'
    first_name = 'John'
    last_name = 'Snow'
    password = factory.PostGenerationMethodCall(
        'set_password', DEFAULT_PASSWORD
    )
