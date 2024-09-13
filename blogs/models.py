from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User  # Import the User model for author field




class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name






class BlogPost(models.Model):
    # Title of the blog post
    title = models.CharField(max_length=200, help_text="Enter the title of the blog post")

    # The main content of the blog post
    content = models.TextField(help_text="Enter the content of the blog post")

    # Foreign key to the User model for the author
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    # Date and time when the post was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Date and time when the post was last updated
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, blank=True, related_name='blog_posts')

    # Metadata (like ordering)
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    # String representation of the model (useful in the admin panel)
    def __str__(self):
        return self.title
        #i want to write return f'{self.author} posted about {self.title}'