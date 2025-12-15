from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import HospitalizationRecordViewSet

router = DefaultRouter()
router.register(r"", HospitalizationRecordViewSet, basename="hospitalizations")

urlpatterns = []

urlpatterns += router.urls
