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
def paginate_queryset(queryset, request, default_page_size=10):
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", default_page_size))

    start = (page - 1) * page_size
    end = start + page_size

    total = queryset.count()
    total_pages = (total + page_size - 1) // page_size

    return {
        "results": queryset[start:end],
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }
