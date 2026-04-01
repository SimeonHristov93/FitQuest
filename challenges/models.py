from django.db import models
from django.contrib.auth.models import User

class Challenge(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    duration_days = models.PositiveIntegerField()
    start_date = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges')
    contestants = models.ManyToManyField(User, through='contestants.ChallengeContestant', related_name='joined_challenges')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
