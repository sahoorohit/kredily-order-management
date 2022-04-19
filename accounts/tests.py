import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class AccountTestMixin:

    def test_when_username_and_password_missing_in_payload__failure(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['username'][0], 'This field is required.')
        self.assertEqual(response_body['password'][0], 'This field is required.')

    def test_when_username_missing_in_payload__failure(self):
        payload = {
            "password": "password"
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['username'][0], 'This field is required.')

    def test_when_password_missing_in_payload__failure(self):
        payload = {
            "username": "johndoe"
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['password'][0], 'This field is required.')

    def test_when_username_length_is_less_than_3__failure(self):
        payload = {
            "username": "jo",
            "password": "password"
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['username'][0], 'Ensure this field has at least 3 characters.')

    def test_when_password_length_is_less_than_6__failure(self):
        payload = {
            "username": "john",
            "password": "pass"
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['password'][0], 'Ensure this field has at least 6 characters.')


class SignUpTest(TestCase, AccountTestMixin):

    @property
    def url(self) -> str:
        return reverse('signup')

    def test_signup__success(self):
        payload = {
            "username": "john",
            "password": "password"
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Sign Up Successful. User Created.')

    def test_when_username_already_taken__failure(self):
        self.test_signup__success()

        payload = {
            "username": "john",
            "password": "new-password"
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['username'], 'Username already taken.')


class LoginTest(TestCase, AccountTestMixin):

    @property
    def url(self) -> str:
        return reverse('login')

    def test_when_credentials_are_invalid(self):
        payload = {
            "username": "john",
            "password": "password"
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Invalid credentials.')

    def test_login__success(self):
        # signing up
        payload = {
            "username": "john",
            "password": "password"
        }
        response = self.client.post(reverse('signup'), data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Sign Up Successful. User Created.')

        # logging in
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Login Successful.')
        self.assertIsNotNone(response_body['token'])
