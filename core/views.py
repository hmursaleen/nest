from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePageView(RedirectView):
    """
    Redirects to the all posts page if the user is logged in,
    or to the login page if not.
    """
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse_lazy('blogs:post_list')  # Redirect to the all posts page
        return reverse_lazy('authentication:login')  # Redirect to the login page
