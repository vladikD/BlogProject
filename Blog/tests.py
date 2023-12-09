from django.test import TestCase
from rest_framework.test import APITestCase

from .models import User
from .serializer import UserRegistrationSerializer


class UserRegistrationAPITests(APITestCase):

    def setUp(self):
        self.valid_data = {
            'email': 'test@gmail.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '12345678',
        }

    def test_registration_success(self):
        response = self.client.post('/api/blog/register/', data=self.valid_data)
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(email='test@gmail.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('12345678'))

    def test_registration_with_invalid_email(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'test'
        response = self.client.post('/api/blog/register/', data=invalid_data)
        self.assertEqual(response.status_code, 400)

        # Перевірка наявності 'email' у відповіді
        self.assertIn('email', response.json())

        # Перевірка тексту помилки, використовуючи 'in'
        expected_error = 'Enter a valid email address.'
        actual_error = response.json()['email'][0]
        self.assertIn(expected_error, actual_error)

    def test_registration_with_too_short_password(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password'] = '123'
        response = self.client.post('/api/blog/register/', data=invalid_data)
        self.assertEqual(response.status_code, 400)

        # Перевірка наявності 'password' у відповіді
        self.assertIn('password', response.json())

        # Перевірка тексту помилки
        self.assertEqual(response.json()['password'][0], 'Пароль повинен бути не менше 8 символів.')

    def test_registration_with_existing_username(self):
        self.client.post('/api/blog/register/', data=self.valid_data)
        response = self.client.post('/api/blog/register/', data=self.valid_data)
        self.assertEqual(response.status_code, 400)

        # Перевірка наявності 'non_field_errors' у відповіді
        self.assertIn('non_field_errors', response.json())

        # Перевірка тексту помилки для 'non_field_errors'
        expected_error = 'Користувач з таким іменем вже існує.'
        actual_error = response.json()['non_field_errors'][0]
        self.assertIn(expected_error, actual_error)

    def test_registration_with_non_gmail_email(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'test@yahoo.com'
        response = self.client.post('/api/blog/register/', data=invalid_data)
        self.assertEqual(response.status_code, 400)

        # Перевірка наявності 'email' у відповіді
        self.assertIn('email', response.json())

        # Перевірка тексту помилки для 'email'
        expected_error = 'Електронна пошта повинна закінчуватися на @gmail.com.'
        actual_error = response.json()['email'][0]
        self.assertIn(expected_error, actual_error)

    def test_registration_with_valid_email(self):
        valid_data = self.valid_data.copy()
        valid_data['email'] = 'test@gmail.com'
        response = self.client.post('/api/blog/register/', data=valid_data)
        self.assertEqual(response.status_code, 201)

        # Перевірка, що користувач був успішно створений
        user = User.objects.get(email='test@gmail.com')
        self.assertEqual(user.email, 'test@gmail.com')

