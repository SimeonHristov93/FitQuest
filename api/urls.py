from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('challenges/', ChallengeListAPI.as_view(), name='challenge-list'),
    path('leaderboard/<int:pk>/', LeaderboardAPI.as_view(), name='leaderboard'),
    path('progress/<int:user_id>/', UserProgressAPI.as_view(), name='user-progress'),
    path('achievements/<int:user_id>/', UserAchievementsAPI.as_view(), name='user-achievements'),
    path('async/challenges/', challenge_list_async_api, name='challenge-list-async'),
    path('async/leaderboard/<int:pk>/', leaderboard_async_api, name='leaderboard-async'),
    path('async/progress/<int:user_id>/', user_progress_async_api, name='user-progress-async'),
    path('async/achievements/<int:user_id>/', user_achievements_async_api, name='user-achievements-async'),
]
