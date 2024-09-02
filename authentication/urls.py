from django.urls import path
from .views import CustomLoginView, SignupView, CustomLogoutView
from django.urls import reverse_lazy


app_name = 'authentication'


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    ]