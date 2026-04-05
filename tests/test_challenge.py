from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User

from challenges.models import Challenge
from contestants.models import ChallengeContestant


class ChallengeModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='creator', password='pass')
        cls.challenge = Challenge.objects.create(
            title='Spring Sprint',
            description='Get moving this spring',
            difficulty='easy',
            duration_days=14,
            start_date=date.today(),
            creator=cls.user,
        )

    def test_str_returns_title(self):
        self.assertEqual(str(self.challenge), 'Spring Sprint')

    def test_creator_related_name_includes_challenge(self):
        self.assertIn(self.challenge, self.user.created_challenges.all())

    def test_contestants_relation_works(self):
        contestant = ChallengeContestant.objects.create(user=self.user, challenge=self.challenge)
        self.assertIn(self.user, self.challenge.contestants.all())
        self.assertEqual(contestant.challenge, self.challenge)
