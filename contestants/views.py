from achievements.utils import check_first_challenge, check_total_reps
from leaderboard.utils import update_leaderboard
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from challenges.models import Challenge
from .models import ChallengeContestant
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import ProgressEntry
from .forms import ProgressEntryForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class LogProgressView(LoginRequiredMixin, CreateView):
    model = ProgressEntry
    form_class = ProgressEntryForm
    template_name = 'contestants/log_progress.html'

    def form_valid(self, form):
        contestant = ChallengeContestant.objects.get(
            user=self.request.user,
            challenge_id=self.kwargs['pk']
        )
        form.instance.contestant = contestant

        response = super().form_valid(form)

        update_leaderboard(contestant.challenge)
        check_total_reps(self.request.user)

        return response

    def get_success_url(self):
        return reverse_lazy('my_challenges')


@login_required
def join_challenge(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)

    contestant, created = ChallengeContestant.objects.get_or_create(
        user=request.user,
        challenge=challenge
    )

    if created:
        check_first_challenge(request.user)

    return redirect('challenge_detail', pk=pk)


@login_required
def leave_challenge(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)

    ChallengeContestant.objects.filter(
        user=request.user,
        challenge=challenge
    ).delete()

    return redirect('challenge_list')


class MyChallengesView(LoginRequiredMixin, ListView):
    model = ChallengeContestant
    template_name = 'contestants/my_challenges.html'
    context_object_name = 'contestants'

    def get_queryset(self):
        return ChallengeContestant.objects.filter(user=self.request.user)
