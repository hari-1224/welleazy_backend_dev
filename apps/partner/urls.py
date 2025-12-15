from django.urls import path
from .views import partner_request

urlpatterns = [
    path("submit/", partner_request, name="partner-submit"),
]
