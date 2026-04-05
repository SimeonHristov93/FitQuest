from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProgressEntry
from leaderboard.utils import update_leaderboard


@receiver(post_save, sender=ProgressEntry)
def refresh_leaderboard_on_progress(sender, instance, **kwargs):
    update_leaderboard(instance.contestant.challenge)
