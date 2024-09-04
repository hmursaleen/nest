from django.views.generic import ListView, UpdateView, DetailView
from .models import Buzz
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views import View


class BuzzListView(LoginRequiredMixin, ListView):
    model = Buzz
    template_name = 'buzz/buzz_list.html'
    context_object_name = 'buzzes'
    paginate_by = 10  # Optional: add pagination for better performance and usability

    def get_queryset(self):
        """
        Filter buzz notifications to only include those for the logged-in user.
        """
        return Buzz.objects.filter(user=self.request.user).order_by('-created_at')











class BuzzDetailView(LoginRequiredMixin, DetailView):
    model = Buzz
    template_name = 'buzz/buzz_detail.html'
    context_object_name = 'buzz'

    def get_object(self, queryset=None):
        """
        Retrieve the Buzz instance and ensure it's for the current user.
        """
        # Get the Buzz instance based on the primary key (pk) from URL
        buzz = get_object_or_404(Buzz, pk=self.kwargs['pk'])

        # Check if the current user is the owner of the buzz notification
        if buzz.user != self.request.user:
            raise PermissionDenied("You do not have permission to view this buzz.")

        # Mark the buzz as read once accessed
        if not buzz.is_read:
            buzz.mark_as_read()

        return buzz













class MarkBuzzAsReadView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Buzz
    fields = []  # No form fields to display or update

    def get_object(self, queryset=None):
        """Retrieve the Buzz instance or return 404."""
        buzz = get_object_or_404(Buzz, pk=self.kwargs['pk'])
        return buzz

    def test_func(self):
        """Ensure that only the owner of the buzz can mark it as read."""
        buzz = self.get_object()
        return self.request.user == buzz.user

    def form_valid(self, form):
        """Mark the buzz as read and redirect to the list view."""
        form.instance.is_read = True
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the list of buzz notifications after marking as read."""
        return reverse_lazy('buzz:buzz_list')

    def handle_no_permission(self):
        """Handle the case where the user does not have permission."""
        return self.redirect_to_list()

    def redirect_to_list(self):
        """Redirect to the list of buzz notifications if no permission."""
        return redirect('buzz:buzz_list')
