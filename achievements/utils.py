from django.db.models import Sum
from .models import UserAchievement
from contestants.models import ChallengeContestant, ProgressEntry
from .models import Achievement

def award_achievement(user, achievement):
    UserAchievement.objects.get_or_create(
        user=user,
        achievement=achievement
    )

def check_first_challenge(user):
    if ChallengeContestant.objects.filter(user=user).exists():
        try:
            achievement = Achievement.objects.get(name="First Challenge Joined")
            award_achievement(user, achievement)
        except Achievement.DoesNotExist:
            pass

def check_total_reps(user):
    total = ProgressEntry.objects.filter(
        contestant__user=user
    ).aggregate(total=Sum('value'))['total'] or 0

    if total >= 1000:
        try:
            achievement = Achievement.objects.get(name="1000 Total Reps")
            award_achievement(user, achievement)
        except Achievement.DoesNotExist:
            pass

    # Check for achievements with required_total_score
    score_achievements = Achievement.objects.filter(required_total_score__gt=0, required_total_score__lte=total)
    for achievement in score_achievements:
        award_achievement(user, achievement)
