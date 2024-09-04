from django.db import models
from django.conf import settings
from blogs.models import BlogPost
from comments.models import Comment

class Buzz(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buzzes')
    trigger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='triggered_buzzes')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Buzz'
        verbose_name_plural = 'Buzzes'

    def __str__(self):
        return f'Buzz for {self.user.username} on {self.post.title} by {self.trigger.username}'

    def mark_as_read(self):
        self.is_read = True
        self.save()
