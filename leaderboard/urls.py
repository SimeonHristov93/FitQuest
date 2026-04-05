from django.urls import path
from .views import LeaderboardView

urlpatterns = [
    path('<int:pk>/', LeaderboardView.as_view(), name='leaderboard'),
]