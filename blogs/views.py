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
from .models import BlogPost

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

# DetailView to display a single blog post
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogs/blogpost_detail.html'
    context_object_name = 'post'

# CreateView to create a new blog post
class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blogs/blogpost_form.html'  # Specify the template to use
    fields = ['title', 'slug', 'content', 'tags', 'status', 'published_at']  # Form fields to include

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        It sets the author to the currently logged-in user before saving.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect to the detail view of the newly created post.
        """
        return reverse_lazy('blogs:post_detail', kwargs={'slug': self.object.slug})

# UpdateView to update an existing blog post
class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    template_name = 'blogs/blogpost_form.html'  # Specify the template to use
    fields = ['title', 'slug', 'content', 'tags', 'status', 'published_at']  # Form fields to include

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
