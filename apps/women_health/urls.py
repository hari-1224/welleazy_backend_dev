
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SymptomViewSet, WomanProfileViewSet, CycleEntryViewSet

router = DefaultRouter()
router.register(r"symptoms", SymptomViewSet, basename="symptom")
router.register(r"profiles", WomanProfileViewSet, basename="profile")
router.register(r"cycles", CycleEntryViewSet, basename="cycle")

urlpatterns = [
    path("", include(router.urls)),
]
