from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    FITNESS_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True, default='', editable=False)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    fitness_level = models.CharField(max_length=20, choices=FITNESS_LEVEL_CHOICES, blank=True, null=True)
    bio = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.user_id:
            self.username = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"
