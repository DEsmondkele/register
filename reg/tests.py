from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    token = refresh.token
    return {
        'refresh': str(refresh),
        'access': str(token),
    }


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.homepage_url = reverse('homepage')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='12345')

    def test_homepage_view(self):
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Welcome to the homepage!'})

    def test_register_view_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_register_view_POST(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'User created successfully.'})

    def test_login_view_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_login_view_POST(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('tokens', response.json())

    def test_login_view_POST_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid credentials.'})

    def test_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Dashboard'})

    def test_dashboard_view_not_authenticated(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 401)  # Unauthorized
