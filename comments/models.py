from django.db import models
from django.conf import settings
from blogs.models import BlogPost  # Import the BlogPost model



class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    #parent: Self-referential ForeignKey to allow comments to have replies. 
    #If parent is None, it’s a top-level comment; otherwise, it’s a reply.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest comments first
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        if self.parent:
            return f'Reply by {self.author} on {self.post.title}'
        return f'Comment by {self.author} on {self.post.title}'

    @property
    def is_reply(self):
        return self.parent is not None
        #is_reply(): Helper method to check if the comment is a reply to another comment.
