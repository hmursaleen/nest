from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Comment
from .forms import CommentForm
from blogs.models import BlogPost
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied




class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_form.html'

    def form_valid(self, form):
        # Assign the author and post to the comment
        form.instance.author = self.request.user
        form.instance.post = self.get_post()
        return super().form_valid(form)

    def form_invalid(self, form):
        # Ensure that the form is returned with errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Redirect back to the post detail page after a comment is added
        return reverse_lazy('blogs:post_detail', kwargs={'pk': self.get_post().pk})

    def get_post(self):
        # Get the post object that this comment is associated with
        return BlogPost.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_post()
        return context


    '''
    form_valid: Automatically sets the author and post fields before saving the form.
    get_success_url: Redirects the user back to the blog post detail page after the comment is submitted.
    get_post: Retrieves the post associated with the comment using the slug from the URL.
    get_context_data: Passes the post object to the template context for displaying post-specific information.
    '''






class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_update_form.html'

    def get_success_url(self):
        # Redirect back to the post detail page after the comment is updated
        return reverse_lazy('blogs:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # Ensure that the user is the author of the comment
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        # Redirect the user to the post detail page if they are not the author
        comment = self.get_object()  # Safely retrieve the comment object
        '''
        afety with get_object:
        get_object() is used to safely retrieve the comment object before handling permissions. 
        This ensures that the post's primary key (pk) is available for the redirection even if 
        the permission test fails.
        '''
        return redirect('blogs:post_detail', pk=comment.post.pk)


        '''
        handle_no_permission Method: This method handles what happens if the user doesn't pass 
        the test_func check. You can customize the response, such as redirecting the user back to the post detail page.
        '''











class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comments/comment_confirm_delete.html'

    def get_object(self, queryset=None):
        """Ensure that only the author can delete the comment."""
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")
        return obj
        '''
        The error you're encountering is due to the get_object method returning an 
        HttpResponseForbidden when the user is not authorized to delete the comment. 
        In such cases, get_success_url is still called after get_object, and because 
        HttpResponseForbidden is returned instead of a Comment object, it fails to 
        access the post attribute, leading to the AttributeError.
        '''

    def get_success_url(self):
        """Redirect to the post detail page after successful deletion."""
        return reverse_lazy('blogs:post_detail', kwargs={'pk': self.object.post.pk})









class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/reply_form.html'

    def form_valid(self, form):
        # Get the parent comment using the provided 'pk' in the URL
        parent_comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        
        # Set the parent, post, and author for the reply
        form.instance.parent = parent_comment
        form.instance.post = parent_comment.post
        form.instance.author = self.request.user
        
        # Call the parent class's form_valid method to save the reply
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print form errors for debugging purposes
        print(form.errors)
        
        # Render the form again with errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Redirect to the blog post detail view after successful reply creation
        return reverse_lazy('blogs:post_detail', kwargs={'pk': self.object.post.pk})

    def get_context_data(self, **kwargs):
        # Add the parent comment to the context for the template
        context = super().get_context_data(**kwargs)
        context['comment'] = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return context








from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer

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
    permission_classes = [IsAuthorOrReadOnly]
    
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
