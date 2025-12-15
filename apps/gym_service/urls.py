from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import GymCenterViewSet, GymPackageViewSet, VoucherViewSet

router = DefaultRouter()
router.register(r'centers', GymCenterViewSet, basename='gymcenter')
router.register(r'packages', GymPackageViewSet, basename='gympackage')
router.register(r'vouchers', VoucherViewSet, basename='voucher')

urlpatterns = [
    path('', include(router.urls)),
]
