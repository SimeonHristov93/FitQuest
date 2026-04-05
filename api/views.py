from asgiref.sync import sync_to_async
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from challenges.models import Challenge
from .serializers import ChallengeSerializer
from rest_framework.permissions import IsAuthenticated
from achievements.models import UserAchievement
from .serializers import AchievementSerializer
from contestants.models import ProgressEntry
from .serializers import ProgressSerializer
from leaderboard.models import LeaderboardEntry
from .serializers import LeaderboardSerializer
from rest_framework.generics import ListAPIView


def _method_not_allowed(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    return None


@sync_to_async
def _auth_meta(request):
    user = request.user
    return user.is_authenticated, user.id, user.is_staff


async def _authorize_user_request(request, user_id):
    is_authenticated, current_user_id, is_staff = await _auth_meta(request)
    if not is_authenticated:
        return None, JsonResponse({'error': 'Authentication required'}, status=401)
    if current_user_id != user_id and not is_staff:
        return None, JsonResponse({"error": "Unauthorized access"}, status=403)
    return current_user_id, None


class ChallengeListAPI(ListAPIView):
        queryset = Challenge.objects.all()
        serializer_class = ChallengeSerializer

        def get_queryset(self):
            difficulty = self.request.GET.get('difficulty')
            qs = Challenge.objects.all()

            if difficulty:
                qs = qs.filter(difficulty=difficulty)

            return qs

class LeaderboardAPI(APIView):
    @staticmethod
    def get(request, pk):
        entries = LeaderboardEntry.objects.filter(challenge_id=pk)
        serializer = LeaderboardSerializer(entries, many=True)
        return Response(serializer.data)

class UserProgressAPI(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, user_id):
        if request.user.id != user_id and not request.user.is_staff:
            return Response({"error": "Unauthorized access"}, status=403)

        entries = ProgressEntry.objects.filter(contestant__user_id=user_id)
        serializer = ProgressSerializer(entries, many=True)
        return Response(serializer.data)

class UserAchievementsAPI(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, user_id):
        if request.user.id != user_id and not request.user.is_staff:
            return Response({"error": "Unauthorized access"}, status=403)

        achievements = UserAchievement.objects.filter(user_id=user_id)
        serializer = AchievementSerializer(achievements, many=True)
        return Response(serializer.data)


async def challenge_list_async_api(request):
    method_error = _method_not_allowed(request)
    if method_error:
        return method_error

    difficulty = request.GET.get('difficulty')

    def fetch():
        qs = Challenge.objects.select_related('creator').prefetch_related('contestants').all()
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        data = []
        for challenge in qs:
            data.append({
                'id': challenge.id,
                'title': challenge.title,
                'description': challenge.description,
                'difficulty': challenge.difficulty,
                'duration_days': challenge.duration_days,
                'start_date': challenge.start_date,
                'created_at': challenge.created_at,
                'creator': str(challenge.creator),
                'contestants': list(challenge.contestants.values_list('id', flat=True)),
            })
        return data

    data = await sync_to_async(fetch)()
    return JsonResponse(data, safe=False)


async def leaderboard_async_api(request, pk):
    method_error = _method_not_allowed(request)
    if method_error:
        return method_error

    data = await sync_to_async(
        lambda: list(
            LeaderboardEntry.objects.filter(challenge_id=pk)
            .select_related('user')
            .values('total_score', 'rank', user_name=F('user__username'))
        )
    )()
    normalized = [
        {'user': row['user_name'], 'total_score': row['total_score'], 'rank': row['rank']}
        for row in data
    ]
    return JsonResponse(normalized, safe=False)


async def user_progress_async_api(request, user_id):
    method_error = _method_not_allowed(request)
    if method_error:
        return method_error

    _, auth_error = await _authorize_user_request(request, user_id)
    if auth_error:
        return auth_error

    data = await sync_to_async(
        lambda: list(
            ProgressEntry.objects.filter(contestant__user_id=user_id)
            .values('day', 'value', 'date_logged')
        )
    )()
    return JsonResponse(data, safe=False)


async def user_achievements_async_api(request, user_id):
    method_error = _method_not_allowed(request)
    if method_error:
        return method_error

    _, auth_error = await _authorize_user_request(request, user_id)
    if auth_error:
        return auth_error

    data = await sync_to_async(
        lambda: list(
            UserAchievement.objects.filter(user_id=user_id)
            .select_related('achievement')
            .values('date_earned', achievement_name=F('achievement__name'))
        )
    )()
    normalized = [
        {'achievement': row['achievement_name'], 'date_earned': row['date_earned']}
        for row in data
    ]
    return JsonResponse(normalized, safe=False)
