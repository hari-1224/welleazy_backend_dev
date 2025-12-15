from django.urls import path, include


from rest_framework.routers import DefaultRouter
from .views import (
    EyeTreatmentViewSet, DentalTreatmentViewSet,
    EyeVendorAddressViewSet, DentalVendorAddressViewSet,
    EyeDentalVoucherViewSet  
)

router = DefaultRouter()

router.register("eye-treatments", EyeTreatmentViewSet)
router.register("dental-treatments", DentalTreatmentViewSet)
router.register("eye-vendors", EyeVendorAddressViewSet, basename="eye-vendors")
router.register("dental-vendors", DentalVendorAddressViewSet, basename="dental-vendors")
router.register("vouchers", EyeDentalVoucherViewSet)




urlpatterns = [
    path('', include(router.urls)),
]
