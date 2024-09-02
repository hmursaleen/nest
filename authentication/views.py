from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View
from .forms import SignupForm



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('blogs:post_list')  # Redirect to the blog post list after successful login







class SignupView(View):
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful signup
            return redirect(reverse_lazy('blogs:post_list'))  # Redirect to the home page or wherever appropriate
        return render(request, self.template_name, {'form': form})








class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to the login page after logout

