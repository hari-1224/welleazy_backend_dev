from django.urls import path
from .views import (
    DependantListCreateView,
    DependantDetailView,
    RelationshipTypeListCreateView,
    SwitchProfileRequestView,
    VerifySwitchOTPView,
    GetActiveProfileView,
    SwitchBackView,
)


urlpatterns = [
    path("relationship-types/", RelationshipTypeListCreateView.as_view(), name="relationship-type-list-create"),
    path("", DependantListCreateView.as_view(), name="dependant-list-create"),
    path("<int:pk>/", DependantDetailView.as_view(), name="dependant-detail"),
    
    # Switch Profile endpoints
    path("switch-profile/request/", SwitchProfileRequestView.as_view(), name="switch-profile-request"),
    path("switch-profile/verify/", VerifySwitchOTPView.as_view(), name="switch-profile-verify"),
    path("active-profile/", GetActiveProfileView.as_view(), name="active-profile"),
    path("switch-back/", SwitchBackView.as_view(), name="switch-back"),
]
