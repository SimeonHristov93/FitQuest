from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User

from achievements.models import Achievement, UserAchievement
from achievements.utils import award_achievement, check_first_challenge
from challenges.models import Challenge
from contestants.models import ChallengeContestant


class AchievementUtilsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='achiever', password='pass')
        self.challenge = Challenge.objects.create(
            title='Starter',
            description='Beginner challenge',
            difficulty='easy',
            duration_days=3,
            start_date=date.today(),
            creator=self.user,
        )

    def test_award_achievement_is_idempotent(self):
        achievement = Achievement.objects.create(
            name='Test Award',
            description='Idempotent check',
            creator=self.user,
        )

        award_achievement(self.user, achievement)
        award_achievement(self.user, achievement)

        self.assertEqual(
            UserAchievement.objects.filter(user=self.user, achievement=achievement).count(),
            1,
        )

    def test_check_first_challenge_grants_achievement(self):
        Achievement.objects.create(
            name='First Challenge Joined',
            description='First join',
            creator=self.user,
        )
        ChallengeContestant.objects.create(user=self.user, challenge=self.challenge)

        check_first_challenge(self.user)

        self.assertTrue(
            self.user.achievements.filter(name='First Challenge Joined').exists()
        )
