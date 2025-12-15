from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import InsurancePolicyRecordViewSet

router = DefaultRouter()
router.register(r"", InsurancePolicyRecordViewSet, basename="insurance-policies")

urlpatterns = router.urls
