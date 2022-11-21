from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from accounts import factories


class UserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.create_user_url = reverse('account:create')
        self.token_url = reverse('account:token')
        self.payload_user = {
            'email': 'test@example.com',
            'password': 'test123',
            'first_name': 'First',
            'last_name': 'Last'
        }
        self.payload_token = {
            'email': 'test@example.com',
            'password': 'test123',
        }

    def test_create_user_success(self):
        resp = self.client.post(self.create_user_url, self.payload_user)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=self.payload_user['email'])
        self.assertTrue(user.check_password(self.payload_user['password']))
        self.assertNotIn('password', resp.data)

    def test_user_with_existing_email(self):
        user = factories.UserFactory(**self.payload_user)
        resp = self.client.post(self.create_user_url, self.payload_user)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_shot(self):
        self.payload_user['password'] = 'test'
        resp = self.client.post(self.create_user_url, self.payload_user)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=self.payload_user['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token(self):
        user = factories.UserFactory(**self.payload_user)
        resp = self.client.post(self.token_url, self.payload_token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('token', resp.data)


    def test_create_token_bad_password(self):
        user = factories.UserFactory(**self.payload_user)
        self.payload_token['password'] = 'incorrect'
        resp = self.client.post(self.token_url, self.payload_token)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', resp.data)
