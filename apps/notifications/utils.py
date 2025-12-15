from .models import Notification

def notify_user(user, title, message, item_type=None):
    # Save only to database (NO Redis, NO WebSocket)
    notif = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        item_type=item_type
    )

    return notif
def paginate_queryset(queryset, request):
    # Simple fallback pagination (no advanced logic)
    page = int(request.GET.get("page", 1))
    page_size = 10

    start = (page - 1) * page_size
    end = start + page_size

    results = queryset[start:end]

    return {
        "results": results,
        "page": page,
        "page_size": page_size,
        "total": queryset.count(),
    }

