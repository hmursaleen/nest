from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView
from .models import Comment, BlogPost
from .forms import CommentForm

class CommentCreateView(FormView):
    form_class = CommentForm
    template_name = 'comments/comment_form.html'  # Create a template to handle the form

    def form_valid(self, form):
        post = get_object_or_404(BlogPost, slug=self.kwargs['slug'])
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()
        return redirect(post.get_absolute_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        parent_comment = None
        if 'parent_id' in self.request.GET:
            parent_comment = get_object_or_404(Comment, id=self.request.GET['parent_id'])
        kwargs['parent'] = parent_comment
        return kwargs
