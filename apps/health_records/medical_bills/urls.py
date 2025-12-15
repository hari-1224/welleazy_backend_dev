from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MedicalBillRecordViewSet

router = DefaultRouter()
router.register(r"", MedicalBillRecordViewSet, basename="medical_bills")

urlpatterns = []

urlpatterns += router.urls
