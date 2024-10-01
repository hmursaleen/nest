from django.urls import path, include
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView, TagDetailView

app_name = 'blogs'

urlpatterns = [
    path('all/', BlogPostListView.as_view(), name='post_list'),  # List all posts
    path('new/', BlogPostCreateView.as_view(), name='post_create'),  # Create a new post
    path('<int:pk>/', BlogPostDetailView.as_view(), name='post_detail'),  # View a single post
    path('<int:pk>/edit/', BlogPostUpdateView.as_view(), name='post_update'),  # Update a post
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),  # Delete a post
    path('tag/<str:name>/', TagDetailView.as_view(), name='tag_detail'),
    ]