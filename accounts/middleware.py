from datetime import timedelta
from django.contrib.auth import logout
from django.utils import timezone


class InactivityLogoutMiddleware:

    TIMEOUT = timedelta(minutes=10)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            last_activity = request.session.get('last_activity')

            if isinstance(last_activity, str):
                try:
                    last_activity = timezone.datetime.fromisoformat(last_activity)
                    if timezone.is_naive(last_activity):
                        last_activity = timezone.make_aware(last_activity, timezone.get_current_timezone())
                except ValueError:
                    last_activity = None

            if last_activity and now - last_activity > self.TIMEOUT:
                logout(request)
                request.session.flush()
            else:
                request.session['last_activity'] = now.isoformat()

        response = self.get_response(request)
        return response
