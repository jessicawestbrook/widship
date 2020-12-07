from django.utils.functional import lazy

from .models import Message


def inbox(request):
    """Provide the count of unread messages for an authenticated user."""
    if request.user.is_authenticated:
        return {'postman_unread_count': lazy(lambda: Message.objects.inbox_unread_count(request.user), int)}
    else:
        return {}
