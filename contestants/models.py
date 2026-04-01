from django.db import models
from django.contrib.auth.models import User
from challenges.models import Challenge

class ChallengeContestant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} in {self.challenge}"

    class Meta:
        unique_together = ('user', 'challenge')

class ProgressEntry(models.Model):
    contestant = models.ForeignKey(ChallengeContestant, on_delete=models.CASCADE)
    day = models.PositiveIntegerField()
    value = models.PositiveIntegerField()  # reps, steps, etc.
    date_logged = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.contestant} - Day {self.day}"
