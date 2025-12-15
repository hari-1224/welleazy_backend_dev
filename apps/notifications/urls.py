from django.urls import path
from .views import UserNotificationsAPIView, MarkNotificationReadAPIView , MarkAllNotificationsReadAPIView

urlpatterns = [
    path("", UserNotificationsAPIView.as_view()),
    path("<int:pk>/read/", MarkNotificationReadAPIView.as_view()),
    path("mark-all-read/", MarkAllNotificationsReadAPIView.as_view()),
]

