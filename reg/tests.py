from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .form import SignUpForm


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.homepage = reverse('homepage')
        self.register = reverse('register')
        self.login = reverse('login')
        self.dashboard = reverse('dashboard')
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_homepage_view(self):
        response = self.client.get(self.homepage)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'reg/index.html')

    def test_register_view_GET(self):
        response = self.client.get(self.register)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'reg/register.html')

    def test_register_view_POST(self):
        response = self.client.post(self.register, {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_login_view_GET(self):
        response = self.client.get(self.login)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'reg/login.html')

    def test_login_view_POST(self):
        response = self.client.post(self.login, {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_view_POST_invalid_credentials(self):
        response = self.client.post(self.login, {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'reg/login.html')

    def test_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.dashboard)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'reg/dashboard.html')

    def test_dashboard_view_not_authenticated(self):
        response = self.client.get(self.dashboard)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
