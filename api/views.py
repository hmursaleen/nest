'''
Creating API Views
DRF allows you to create API views in several ways. The most common approach 
is to use viewsets, which automatically provide implementations for CRUD operations.
'''


from .serializers import BlogPostSerializer, TagSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, permissions, status
from comments.models import Comment
from blogs.models import BlogPost, Tag



'''
viewsets.ModelViewSet: Provides default implementations for list, create, 
retrieve, update, and destroy actions.

In Django REST Framework, a ViewSet is typically written for each model, not for each view. 
A ViewSet provides a way to combine the logic for multiple HTTP methods (like GET, POST, PUT, 
DELETE) into a single class. It can handle a set of operations (like listing, retrieving, 
creating, updating, and deleting instances of a model) in one place.

Here's how it works:

ModelViewSet: A common type of ViewSet that handles all the standard actions (list, create, 
retrieve, update, and delete) for a model.
So, instead of writing separate views for listing all blog posts, retrieving a single 
blog post, creating a new blog post, etc., you can write a single ViewSet for the 
BlogPost model. This ViewSet will automatically provide all the necessary views.

permission_classes: Specifies the permissions. Here, we're using IsAuthenticatedOrReadOnly.

perform_create: Overrides the default behavior to associate the currently 
logged-in user as the author of a blog post.
'''





class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]  # Use JWTAuthentication
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]  # Ensure permissions are set properly

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.author:
            serializer.save()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)







class TagViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing tag instances.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [JWTAuthentication, SessionAuthentication]  # Use JWTAuthentication
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]  # Ensure permissions are set properly

    def perform_create(self, serializer):
        """
        Override this method if you want to customize the creation logic.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Override this method if you want to customize the update logic.
        """
        serializer.save()











class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a comment to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the comment
        return obj.author == request.user






class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]  # Use JWTAuthentication
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]  # Ensure permissions are set properly

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.author:
            serializer.save()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        if self.request.user == instance.author:
            instance.delete()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

