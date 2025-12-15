from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    VaccinationCertificateRecordViewSet,
)

router = DefaultRouter()
router.register(r"", VaccinationCertificateRecordViewSet, basename="vaccination_certificates")

urlpatterns = []

urlpatterns += router.urls
