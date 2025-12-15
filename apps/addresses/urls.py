# apps/addresses/urls.py
from django.urls import path
from .views import (
    AddressTypeListCreateView,
    SelfAddressListCreateView,
    SelfAddressDetailView,
    DependantAddressListCreateView,
    DependantAddressDetailView,
    UnifiedAddressListCreateView,
    UnifiedAddressDetailView,
)


urlpatterns = [
    path("types/", AddressTypeListCreateView.as_view(), name="address-type-list-create"),

    # Self
    path("self/", SelfAddressListCreateView.as_view(), name="self-address-list-create"),
    path("self/<int:pk>/", SelfAddressDetailView.as_view(), name="self-address-detail"),

    # Dependant (Nested)
    path("dependants/<int:dependant_id>/addresses/", DependantAddressListCreateView.as_view(),
         name="dependant-address-list-create"),

    path("dependants/<int:dependant_id>/addresses/<int:pk>/", DependantAddressDetailView.as_view(),
         name="dependant-address-detail"),
    
    # Unified API (Works with Profile Switching)
    path("", UnifiedAddressListCreateView.as_view(), name="unified-address-list-create"),
    path("<int:pk>/", UnifiedAddressDetailView.as_view(), name="unified-address-detail"),
]

