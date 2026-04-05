from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile


class ProfileModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='pass')

    def test_save_syncs_username(self):
        profile = self.user.profile
        self.user.username = 'updated'
        self.user.save()

        profile.save()

        self.assertEqual(profile.username, 'updated')

    def test_str_contains_username(self):
        profile = self.user.profile

        self.assertEqual(str(profile), f"{self.user.username}'s Profile")
