from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.utils import create_notification

from .models import UserAchievement


@receiver(post_save, sender=UserAchievement)
def notify_on_achievement_awarded(sender, instance, created, **kwargs):
    if not created:
        return

    achievement = instance.achievement
    create_notification(
        user=instance.user,
        title=f"Achievement unlocked: {achievement.name}",
        message=achievement.description or "You earned a new achievement.",
    )
