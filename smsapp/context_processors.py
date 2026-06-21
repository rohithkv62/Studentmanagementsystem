from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            notifs = Notification.objects.filter(user__isnull=True).order_by('-created_at')[:10]
            unread_count = Notification.objects.filter(user__isnull=True, is_read=False).count()
        else:
            notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
            unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'navbar_notifications': notifs, 'unread_notif_count': unread_count}
    return {}
