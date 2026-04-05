from django.db import models
from django.contrib.auth import get_user_model


class Notification(models.Model):
    GENERAL = 'general'
    LEADERBOARD = 'leaderboard'

    NOTIFICATION_TYPES = [
        (GENERAL, 'General'),
        (LEADERBOARD, 'Leaderboard'),
    ]

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=120)
    message = models.TextField(blank=True)
    notification_type = models.CharField(
        max_length=32,
        choices=NOTIFICATION_TYPES,
        default=GENERAL
    )
    challenge = models.ForeignKey(
        'challenges.Challenge',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} — {self.title}"
