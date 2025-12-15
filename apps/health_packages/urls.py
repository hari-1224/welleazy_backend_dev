from rest_framework.routers import DefaultRouter
from .views import HealthPackageViewSet

router = DefaultRouter()
router.register(r'packages', HealthPackageViewSet, basename='healthpackage')

urlpatterns = router.urls
