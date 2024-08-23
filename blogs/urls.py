# blogs/urls.py

from django.urls import path, include
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = 'blogs'

urlpatterns = [
    path('all/', BlogPostListView.as_view(), name='post_list'),  # List all posts
    path('new/', BlogPostCreateView.as_view(), name='post_create'),  # Create a new post
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='post_detail'),  # View a single post
    path('<slug:slug>/edit/', BlogPostUpdateView.as_view(), name='post_update'),  # Update a post
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),  # Delete a post
]


from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, TagViewSet

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet)
router.register(r'tags', TagViewSet)

urlpatterns += [
    path('', include(router.urls)),
]

'''
DefaultRouter: Automatically generates the URLs for the registered viewsets.
router.register: Registers the viewsets with the router.
'''