from .models import Notification


def create_notification(user, title, message='', notification_type=Notification.GENERAL, challenge=None):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        challenge=challenge,
    )
