from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from challenges.models import Challenge
from contestants.models import ChallengeContestant
from leaderboard.models import LeaderboardEntry


class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='viewer', password='pass')
        self.easy_challenge = Challenge.objects.create(
            title='Easy Go',
            description='Relaxed challenge',
            difficulty='easy',
            duration_days=3,
            start_date=date.today(),
            creator=self.user,
        )
        self.hard_challenge = Challenge.objects.create(
            title='Hard Go',
            description='Intense challenge',
            difficulty='hard',
            duration_days=5,
            start_date=date.today(),
            creator=self.user,
        )

    def test_challenge_list_filters_by_difficulty(self):
        response = self.client.get(reverse('challenge_list'), {'difficulty': 'hard'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['challenges']), [self.hard_challenge])

    def test_challenge_detail_context_marks_contestant(self):
        ChallengeContestant.objects.create(user=self.user, challenge=self.easy_challenge)
        self.client.login(username='viewer', password='pass')

        response = self.client.get(reverse('challenge_detail', args=[self.easy_challenge.pk]))

        self.assertTrue(response.context.get('is_contestant'))

    def test_leaderboard_view_context_includes_challenge(self):
        entry = LeaderboardEntry.objects.create(
            user=self.user,
            challenge=self.easy_challenge,
            total_score=50,
            rank=1,
        )

        response = self.client.get(reverse('leaderboard:leaderboard', args=[self.easy_challenge.pk]))

        self.assertEqual(response.context['challenge'], self.easy_challenge)
        self.assertIn(entry, response.context['entries'])
