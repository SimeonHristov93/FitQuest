from django.urls import path
from .views import *

urlpatterns = [
    path('', ChallengeListView.as_view(), name='challenge_list'),
    path('<int:pk>/', ChallengeDetailView.as_view(), name='challenge_detail'),
    path('create/', ChallengeCreateView.as_view(), name='challenge_create'),
    path('<int:pk>/edit/', ChallengeUpdateView.as_view(), name='challenge_edit'),
    path('<int:pk>/delete/', ChallengeDeleteView.as_view(), name='challenge_delete'),
]