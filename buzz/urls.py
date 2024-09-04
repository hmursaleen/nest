from django.urls import path
from .views import BuzzListView, MarkBuzzAsReadView, BuzzDetailView

app_name = 'buzz'

urlpatterns = [
    path('all/', BuzzListView.as_view(), name='buzz_list'),
    path('mark_as_read/<int:pk>/', MarkBuzzAsReadView.as_view(), name='mark_buzz_as_read'),
    path('<int:pk>/', BuzzDetailView.as_view(), name='buzz_detail'),
]
