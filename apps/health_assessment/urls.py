from rest_framework.routers import DefaultRouter
from .views import HealthAssessmentViewSet

router = DefaultRouter()
router.register(r"", HealthAssessmentViewSet, basename="health-assessments")

urlpatterns = router.urls
