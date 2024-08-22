from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomLoginForm

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('blogs:post_list')  # Redirect to the blog post list after successful login
