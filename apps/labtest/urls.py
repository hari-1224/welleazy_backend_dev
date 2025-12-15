from rest_framework.routers import DefaultRouter
from .views import TestViewSet
# from .views import DiagnosticCenterViewSet
# from .views import DiagnosticCenterSearchAPIView
from django.urls import path


router = DefaultRouter()
router.register(r'tests', TestViewSet, basename='test')
# router.register(r'diagnostic-centers', DiagnosticCenterViewSet, basename='diagnosticcenter')

# urlpatterns = [
#     path('search-centers/', DiagnosticCenterSearchAPIView.as_view(), name='search-centers'),
# ]
urlpatterns = router.urls