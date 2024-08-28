from django.urls import path
from .views import CommentCreateView

app_name = 'comments'

urlpatterns = [
    path('post/<slug:slug>/comment/', CommentCreateView.as_view(), name='add_comment'),
]
