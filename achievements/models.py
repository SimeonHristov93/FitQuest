from django.db import models
from django.contrib.auth.models import User

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_achievements')
    icon = models.ImageField(upload_to='achievements/', blank=True, null=True)
    required_total_score = models.PositiveIntegerField(default=0, help_text="Total score required to earn this achievement automatically. Set to 0 for manual/hardcoded awards.")
    users = models.ManyToManyField(User, through='UserAchievement', related_name='achievements')

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} earned {self.achievement}"

    class Meta:
        unique_together = ('user', 'achievement')
