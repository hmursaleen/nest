from .models import Buzz

def unread_buzz_count(request):
    if request.user.is_authenticated:
        count = Buzz.objects.filter(user=request.user, is_read=False).count()
        return {'unread_buzz_count': count}
    return {'unread_buzz_count': 0}
