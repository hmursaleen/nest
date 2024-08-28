from django.urls import path
from .views import CommentCreateView, CommentUpdateView

app_name = 'comments'

urlpatterns = [
    path('comment/post/<slug:slug>', CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
]
