from django.urls import path
from .views import *

urlpatterns = [
    path('join/<int:pk>/', join_challenge, name='join_challenge'),
    path('leave/<int:pk>/', leave_challenge, name='leave_challenge'),
    path('my-challenges/', MyChallengesView.as_view(), name='my_challenges'),
    path('log/<int:pk>/', LogProgressView.as_view(), name='log_progress'),
]