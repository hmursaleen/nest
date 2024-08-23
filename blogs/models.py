# blogs/models.py

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

    '''
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blogs:tag_detail', kwargs={'name': self.name})
    '''







class BlogPost(models.Model):
    # Title of the blog post
    title = models.CharField(max_length=200, help_text="Enter the title of the blog post")

    # Slug for the blog post (useful for URLs)
    slug = models.SlugField(unique=True, max_length=200)

    # The main content of the blog post
    content = models.TextField(help_text="Enter the content of the blog post")

    # Foreign key to the User model for the author
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    # Date and time when the post was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Date and time when the post was last updated
    updated_at = models.DateTimeField(auto_now=True)

    # Optional: Published date (if you want to control when posts go live)

    is_published = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, blank=True, related_name='blog_posts')

    published_at = models.DateTimeField(blank=True, null=True)

    # Optional: A field to manage the status of the post (draft or published)
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # Metadata (like ordering)
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    # String representation of the model (useful in the admin panel)
    def __str__(self):
        return self.title
        #i want to write return f'{self.author} posted about {self.title}'

    # Method to get the absolute URL of a blog post (useful for linking)
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blogs:post_detail', kwargs={'slug': self.slug})


    def publish(self):
        self.is_published = True
        #self.published_at = models.DateTimeField(auto_now_add=True)
        self.save()