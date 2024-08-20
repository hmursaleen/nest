# blogs/urls.py

from django.urls import path
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = 'blogs'

urlpatterns = [
    path('', BlogPostListView.as_view(), name='post_list'),  # List all posts
    path('post/<slug:slug>/', BlogPostDetailView.as_view(), name='post_detail'),  # View a single post
    path('post/new/', BlogPostCreateView.as_view(), name='post_create'),  # Create a new post
    path('post/<slug:slug>/edit/', BlogPostUpdateView.as_view(), name='post_update'),  # Update a post
    path('post/<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),  # Delete a post
]
