from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PrescriptionRecordViewSet,
)

router = DefaultRouter()
router.register(r"", PrescriptionRecordViewSet, basename="prescriptions")

urlpatterns = []

urlpatterns += router.urls
