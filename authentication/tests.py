from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_view(self):
        response = self.client.get(reverse('authentication:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_success(self):
        login = self.client.login(username='testuser', password='password123')
        self.assertTrue(login)

    def test_login_failure(self):
        login = self.client.login(username='testuser', password='wrongpassword')
        self.assertFalse(login)
