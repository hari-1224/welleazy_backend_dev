from rest_framework.routers import DefaultRouter
from .views import VisitTypeViewSet
from django.urls import path
from .views import DiagnosticCenterFilterAPIView

router = DefaultRouter()
router.register(r'visit-types', VisitTypeViewSet, basename='visit-type')

urlpatterns = [
    path('diagnostic-center/search', DiagnosticCenterFilterAPIView.as_view(), name='diagnostic-center-search'),
]

urlpatterns += router.urls
