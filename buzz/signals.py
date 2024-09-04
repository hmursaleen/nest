from django.db.models.signals import post_save
from django.dispatch import receiver
from comments.models import Comment
from .models import Buzz

@receiver(post_save, sender=Comment)
def create_buzz_on_comment(sender, instance, created, **kwargs):
    """
    Signal to create a Buzz when a new comment is added to a user's post.
    """
    if created and instance.post.author != instance.author:
        # Ensure the buzz is only created if the comment author is different from the post author
        Buzz.objects.create(
            user=instance.post.author,         # The user who will receive the buzz
            trigger=instance.author,           # The user who triggered the buzz
            post=instance.post,
            comment=instance,
            is_read=False
        )

'''
@receiver(post_save, sender=Comment): This decorator connects the create_buzz_on_comment function 
to the post_save signal of the Comment model.

The signal function checks if a new comment is created (created=True) and if the comment author 
is not the post author. If both conditions are met, a Buzz is created.
'''