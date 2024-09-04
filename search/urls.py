from django.urls import path
from .views import SearchView, search_ajax

app_name = 'search'

urlpatterns = [
    path('results/', SearchView.as_view(), name='search'),
    path('ajax/', search_ajax, name='search_ajax'),
]
