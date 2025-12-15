from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicineReminderViewSet

router = DefaultRouter()
router.register(r"", MedicineReminderViewSet, basename="medicine-reminders")

urlpatterns = router.urls
