# blogs/views.py

'''
Ensure that only authenticated users can create, edit, or delete posts. 
This can be enforced using Django’s built-in decorators or mixins like 
LoginRequiredMixin and UserPassesTestMixin.

LoginRequiredMixin ensures that only logged-in users can access the view.

UserPassesTestMixin allows you to write custom logic to check whether a 
user has permission to perform a certain action 
(e.g., only the author of a blog post can edit or delete it).

The test_func() method is used in conjunction with UserPassesTestMixin 
to specify the condition that must be met for the user to pass the test.
'''
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost, Tag
from .forms import BlogPostForm, BlogPostUpdateForm
from django.shortcuts import get_object_or_404

# ListView to display all published blog posts
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogs/blogpost_list.html'  # Specify the template to use
    context_object_name = 'posts'  # Name of the context variable to use in the template
    paginate_by = 10  # Number of posts per page

    def get_queryset(self):
        """
        Override this method to filter the queryset to only show published posts,
        ordered by creation date in descending order.
        """
        return BlogPost.objects.filter(status='published').order_by('-created_at')



class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogs/blogpost_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(parent__isnull=True)  # Get top-level comments
        return context




# CreateView to create a new blog post
class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogs/blogpost_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogs:post_detail', kwargs={'slug': self.object.slug})







# UpdateView to update an existing blog post
class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostUpdateForm  # Use the custom form
    template_name = 'blogs/blogpost_update_form.html'  # Specify the template to use

    def get_success_url(self):
        """
        Redirect to the detail view of the updated post.
        """
        return reverse_lazy('blogs:post_detail', kwargs={'slug': self.object.slug})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author





# DeleteView to delete a blog post
class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blogs/blogpost_confirm_delete.html'  # Specify the template to use

    def get_success_url(self):
        """
        Redirect to the list view of blog posts after successful deletion.
        """
        return reverse_lazy('blogs:post_list')


    def test_func(self):
    	post = self.get_object()
    	return self.request.user == post.author











class TagDetailView(ListView):
    model = BlogPost
    template_name = 'blogs/tag_detail.html'  # Specify the template to use
    context_object_name = 'posts'
    paginate_by = 10  # If you want to paginate the posts

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, name=self.kwargs['name'])
        return BlogPost.objects.filter(tags=self.tag).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


'''
Creating API Views
DRF allows you to create API views in several ways. The most common approach 
is to use viewsets, which automatically provide implementations for CRUD operations.
'''


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import BlogPostSerializer, TagSerializer


'''
viewsets.ModelViewSet: Provides default implementations for list, create, 
retrieve, update, and destroy actions.

permission_classes: Specifies the permissions. Here, we're using IsAuthenticatedOrReadOnly.

perform_create: Overrides the default behavior to associate the currently 
logged-in user as the author of a blog post.
'''

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
