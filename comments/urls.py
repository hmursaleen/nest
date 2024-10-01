from django.urls import path, include
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView, ReplyCreateView

app_name = 'comments'

urlpatterns = [
    path('post/<int:pk>', CommentCreateView.as_view(), name='add_comment'),
    path('<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('<int:pk>/reply/', ReplyCreateView.as_view(), name='reply_comment'),
]
