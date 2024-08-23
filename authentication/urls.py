from django.urls import path
from .views import CustomLoginView, SignupView
from django.contrib.auth.views import LogoutView


app_name = 'authentication'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='authentication:login'), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    ]