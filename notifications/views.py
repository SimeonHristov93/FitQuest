from asgiref.sync import sync_to_async
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render

from .models import Notification


async def notification_list_view(request):
    is_authenticated, user_id = await sync_to_async(
        lambda: (request.user.is_authenticated, request.user.id)
    )()
    if not is_authenticated:
        return redirect_to_login(request.get_full_path())

    notifications = await sync_to_async(list)(
        Notification.objects.filter(user_id=user_id)
    )
    await sync_to_async(
        lambda: Notification.objects.filter(user_id=user_id, read=False).update(read=True)
    )()
    return await sync_to_async(render)(
        request,
        'notifications/list.html',
        {'notifications': notifications},
    )
