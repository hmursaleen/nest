from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, TagViewSet, CommentViewSet

app_name = 'api'




'''
DefaultRouter: Automatically generates the URLs for the registered viewsets.
router.register: Registers the viewsets with the router.
'''

router = DefaultRouter()

router.register(r'posts', BlogPostViewSet)
router.register(r'tags', TagViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 