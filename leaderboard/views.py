from django.shortcuts import get_object_or_404
from challenges.models import Challenge
from django.views.generic import ListView
from .models import LeaderboardEntry

class LeaderboardView(ListView):
    model = LeaderboardEntry
    template_name = 'leaderboard/leaderboard.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return LeaderboardEntry.objects.filter(
            challenge_id=self.kwargs['pk']
        ).select_related('user').order_by('rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenge'] = get_object_or_404(Challenge, pk=self.kwargs['pk'])
        return context