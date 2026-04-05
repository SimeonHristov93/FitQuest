from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from challenges.models import Challenge
from contestants.models import ChallengeContestant
from achievements.models import Achievement


class ParticipationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='participant', password='pass')
        self.challenge = Challenge.objects.create(
            title='Daily Push',
            description='Push your limits',
            difficulty='medium',
            duration_days=7,
            start_date=date.today(),
            creator=self.user,
        )
        self.client.login(username='participant', password='pass')

    def test_join_challenge_creates_contestant(self):
        response = self.client.get(reverse('join_challenge', args=[self.challenge.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ChallengeContestant.objects.filter(user=self.user, challenge=self.challenge).exists()
        )

    def test_join_challenge_awards_first_challenge(self):
        Achievement.objects.create(
            name='First Challenge Joined',
            description='Joined first challenge',
            creator=self.user,
        )

        self.client.get(reverse('join_challenge', args=[self.challenge.pk]))
        self.assertTrue(
            self.user.achievements.filter(name='First Challenge Joined').exists()
        )

    def test_leave_challenge_removes_contestant(self):
        ChallengeContestant.objects.create(user=self.user, challenge=self.challenge)
        self.assertEqual(ChallengeContestant.objects.count(), 1)

        response = self.client.get(reverse('leave_challenge', args=[self.challenge.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            ChallengeContestant.objects.filter(user=self.user, challenge=self.challenge).exists()
        )
