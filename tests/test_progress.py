from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User

from contestants.models import ChallengeContestant, ProgressEntry
from contestants.forms import ProgressEntryForm
from challenges.models import Challenge
from achievements.utils import check_total_reps
from achievements.models import Achievement


class ProgressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='progressor', password='pass')
        self.challenge = Challenge.objects.create(
            title='Step Up',
            description='Daily steps',
            difficulty='easy',
            duration_days=5,
            start_date=date.today(),
            creator=self.user,
        )
        self.contestant = ChallengeContestant.objects.create(user=self.user, challenge=self.challenge)

    def test_progress_entry_str(self):
        entry = ProgressEntry.objects.create(
            contestant=self.contestant,
            day=1,
            value=50,
        )

        self.assertEqual(str(entry), f"{self.contestant} - Day 1")

    def test_progress_entry_form_validates_day(self):
        form = ProgressEntryForm(data={'day': 0, 'value': 20})
        self.assertFalse(form.is_valid())
        self.assertIn('day', form.errors)

    def test_check_total_reps_awards_threshold(self):
        Achievement.objects.create(
            name='1000 Total Reps',
            description='Milestone',
            creator=self.user,
        )

        ProgressEntry.objects.create(contestant=self.contestant, day=1, value=500)
        ProgressEntry.objects.create(contestant=self.contestant, day=2, value=600)

        check_total_reps(self.user)

        self.assertTrue(self.user.achievements.filter(name='1000 Total Reps').exists())
