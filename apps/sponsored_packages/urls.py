from rest_framework.routers import DefaultRouter
from .views import SponsoredPackageViewSet

router = DefaultRouter()
router.register(r'packages', SponsoredPackageViewSet, basename='sponsoredpackage')

urlpatterns = router.urls
