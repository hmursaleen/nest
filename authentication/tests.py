from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import SignupForm


class LoginViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_view(self):
        response = self.client.get(reverse('authentication:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

    def test_login_success(self):
        login = self.client.login(username='testuser', password='password123')
        self.assertTrue(login)

    def test_login_failure(self):
        login = self.client.login(username='testuser', password='wrongpassword')
        self.assertFalse(login)




  # Make sure to import your form

class SignupViewTest(TestCase):
    def setUp(self):
        self.signup_url = reverse('signup')

    def test_signup_view_get(self):
        """Test GET request to the signup view returns a form."""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/signup.html')
        self.assertIsInstance(response.context['form'], SignupForm)

    def test_signup_view_post_valid(self):
        """Test POST request with valid data successfully signs up a user."""
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blogs:post_list'))
        user = get_user_model().objects.get(username='testuser')
        self.assertTrue(user)

    def test_signup_view_post_invalid(self):
        """Test POST request with invalid data re-renders the form with errors."""
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'wrongpassword123',  # Passwords don't match
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/signup.html')

        # Check if the form is bound and has errors
        form = response.context['form']
        self.assertTrue(form.is_bound)
        self.assertTrue(form.errors)
        self.assertFalse(get_user_model().objects.filter(username='testuser').exists())
        self.assertFormError(response, 'form', 'password2', "The two password fields didn't match.")









class CustomLogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_logout_view_redirect(self):
        """Test that a logged-in user is logged out and redirected to the login page."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_logout_view_logged_out(self):
        """Test that a logged-out user cannot access a restricted page."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.client.logout()  # Ensure user is logged out

        # Try to access a restricted page (if any)
        response = self.client.get(reverse('blogs:post_list'))
        self.assertNotContains(response, 'Logout')  # Ensure the user is logged out

