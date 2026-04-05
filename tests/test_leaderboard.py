from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User

from challenges.models import Challenge
from contestants.models import ChallengeContestant, ProgressEntry
from leaderboard.utils import update_leaderboard
from leaderboard.models import LeaderboardEntry


class LeaderboardTests(TestCase):
    def setUp(self):
        self.challenge = Challenge.objects.create(
            title='Rank Battle',
            description='Climb the board',
            difficulty='hard',
            duration_days=10,
            start_date=date.today(),
            creator=User.objects.create_user(username='creator2', password='pass'),
        )
        self.user_one = User.objects.create_user(username='u1', password='pass')
        self.user_two = User.objects.create_user(username='u2', password='pass')
        self.contestant_one = ChallengeContestant.objects.create(user=self.user_one, challenge=self.challenge)
        self.contestant_two = ChallengeContestant.objects.create(user=self.user_two, challenge=self.challenge)

    def test_update_leaderboard_creates_ranked_entries(self):
        ProgressEntry.objects.create(contestant=self.contestant_one, day=1, value=30)
        ProgressEntry.objects.create(contestant=self.contestant_two, day=1, value=10)

        update_leaderboard(self.challenge)

        entries = LeaderboardEntry.objects.filter(challenge=self.challenge).order_by('rank')
        self.assertEqual(entries.count(), 2)
        self.assertEqual(entries.first().user, self.user_one)
        self.assertEqual(entries.first().rank, 1)

    def test_update_leaderboard_updates_scores_and_ranks(self):
        ProgressEntry.objects.create(contestant=self.contestant_one, day=1, value=5)
        ProgressEntry.objects.create(contestant=self.contestant_two, day=1, value=15)

        update_leaderboard(self.challenge)

        ProgressEntry.objects.create(contestant=self.contestant_one, day=2, value=50)
        update_leaderboard(self.challenge)

        top_entry = LeaderboardEntry.objects.get(challenge=self.challenge, user=self.user_one)
        self.assertEqual(top_entry.rank, 1)
        self.assertGreaterEqual(top_entry.total_score, 55)
