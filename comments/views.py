from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Comment
from .forms import CommentForm
from blogs.models import BlogPost
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 




class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

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
        return reverse_lazy('blogs:post_detail', kwargs={'slug': self.get_post().slug})

    def get_post(self):
        # Get the post object that this comment is associated with
        return BlogPost.objects.get(slug=self.kwargs['slug'])

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
    template_name = 'comment_update_form.html'

    def get_success_url(self):
        # Redirect back to the post detail page after the comment is updated
        return reverse_lazy('blogs:post_detail', kwargs={'slug': self.object.post.slug})

    def test_func(self):
        # Ensure that the user is the author of the comment
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        # Customize the response if the user fails the test (e.g., redirect to the post)
        return reverse_lazy('blogs:post_detail', kwargs={'slug': self.get_object().post.slug})

        '''
        handle_no_permission Method: This method handles what happens if the user doesn't pass 
        the test_func check. You can customize the response, such as redirecting the user back to the post detail page.
        '''







from django.http import HttpResponseForbidden

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def get_object(self, queryset=None):
        """Ensure that only the author can delete the comment."""
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            return HttpResponseForbidden("You do not have permission to delete this comment.")
        return obj

    def get_success_url(self):
        """Redirect to the post detail page after successful deletion."""
        return reverse_lazy('blogs:post_detail', kwargs={'slug': self.object.post.slug})

