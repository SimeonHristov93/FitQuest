from django.shortcuts import get_object_or_404

from .models import Challenge


class ChallengeContextMiddleware:

    CHALLENGE_VIEW_NAMES = {
        'challenge_detail',
        'challenge_edit',
        'challenge_delete',
        'join_challenge',
        'leave_challenge',
        'log_progress',
        'leaderboard:leaderboard',
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.challenge = None
        request.is_challenge_member = False
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        pk = view_kwargs.get('pk')
        match = getattr(request, 'resolver_match', None)
        view_name = match.view_name if match else ''

        if pk is None or view_name not in self.CHALLENGE_VIEW_NAMES:
            return None

        challenge = get_object_or_404(Challenge, pk=pk)
        request.challenge = challenge

        user = request.user
        if user.is_authenticated:
            request.is_challenge_member = challenge.contestants.filter(id=user.id).exists()

        return None
