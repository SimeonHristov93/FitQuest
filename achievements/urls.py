from django.urls import path
from .views import (
    AchievementListView,
    UserAchievementView,
    AchievementCreateView,
    AchievementUpdateView,
    AchievementDeleteView,
    MyAchievementsRedirectView,
)

urlpatterns = [
    path('', AchievementListView.as_view(), name='all_achievements'),
    path('my-achievements/', MyAchievementsRedirectView.as_view(), name='my_achievements'),
    path('add/', AchievementCreateView.as_view(), name='achievement_add'),
    path('<int:pk>/edit/', AchievementUpdateView.as_view(), name='achievement_edit'),
    path('<int:pk>/delete/', AchievementDeleteView.as_view(), name='achievement_delete'),
    path('<str:username>/', UserAchievementView.as_view(), name='my_achievements'),
]
