from rest_framework.routers import DefaultRouter
from .views import SiteFeedbackViewSet

router = DefaultRouter()
router.register(r"site-feedback", SiteFeedbackViewSet, basename="site-feedback")

urlpatterns = router.urls
