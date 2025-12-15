# apps/care_programs/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CareProgramBookingViewSet

router = DefaultRouter()
router.register(r"bookings", CareProgramBookingViewSet, basename="care-program-booking")

urlpatterns = [
    path("", include(router.urls)),
]
