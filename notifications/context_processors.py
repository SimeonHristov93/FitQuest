from .models import Notification


def notification_counts(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, read=False).count()
    else:
        count = 0
    return {'notification_unread_count': count}
