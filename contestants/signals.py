from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.utils import create_notification

from .models import ProgressEntry, ChallengeContestant
from leaderboard.utils import update_leaderboard


@receiver(post_save, sender=ProgressEntry)
def refresh_leaderboard_on_progress(sender, instance, **kwargs):
    update_leaderboard(instance.contestant.challenge)


@receiver(post_save, sender=ChallengeContestant)
def notify_on_challenge_join(sender, instance, created, **kwargs):
    if not created:
        return

    create_notification(
        user=instance.user,
        title=f"Joined challenge: {instance.challenge.title}",
        message=f"You are now participating in '{instance.challenge.title}'.",
        challenge=instance.challenge,
    )
