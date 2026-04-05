from django.db.models import Sum
from contestants.models import ProgressEntry, ChallengeContestant
from .models import LeaderboardEntry

def update_leaderboard(challenge):
    contestants = ChallengeContestant.objects.filter(challenge=challenge)

    leaderboard_data = []

    for contestant in contestants:
        total = ProgressEntry.objects.filter(
            contestant=contestant
        ).aggregate(total=Sum('value'))['total'] or 0

        leaderboard_data.append({
            'user': contestant.user,
            'total': total
        })

    leaderboard_data.sort(key=lambda x: x['total'], reverse=True)

    for index, entry in enumerate(leaderboard_data, start=1):
        LeaderboardEntry.objects.update_or_create(
            user=entry['user'],
            challenge=challenge,
            defaults={
                'total_score': entry['total'],
                'rank': index
            }
        )
