from rest_framework import serializers
from challenges.models import Challenge
from contestants.models import ProgressEntry
from leaderboard.models import LeaderboardEntry
from achievements.models import UserAchievement

class ChallengeSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = Challenge
        fields = '__all__'

class LeaderboardSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = LeaderboardEntry
        fields = ['user', 'total_score', 'rank']

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressEntry
        fields = ['day', 'value', 'date_logged']


class AchievementSerializer(serializers.ModelSerializer):
    achievement = serializers.StringRelatedField()

    class Meta:
        model = UserAchievement
        fields = ['achievement', 'date_earned']