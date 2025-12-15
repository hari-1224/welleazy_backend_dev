from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import requests

from apps.diagnostic_center.models import DiagnosticCenter
from apps.diagnostic_center.serializers import DiagnosticCenterSerializer
from apps.location.models import City

from apps.health_packages.models import HealthPackage
from apps.sponsored_packages.models import SponsoredPackage

class DiagnosticCenterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DiagnosticCenter.objects.filter(deleted_at__isnull=True)
    serializer_class = DiagnosticCenterSerializer

    def list(self, request):
        client_api_url = getattr(settings, "CLIENT_DIAGNOSTIC_API_URL", None)
        if client_api_url:
            try:
                headers = {}
                client_api_token = getattr(settings, "CLIENT_API_TOKEN", None)
                if client_api_token:
                    headers["Authorization"] = f"Bearer {client_api_token}"

                response = requests.get(client_api_url, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()

                formatted_data = [
                    {
                        "id": item.get("id"),
                        "name": item.get("center_name") or item.get("name"),
                        "code": item.get("code"),
                        "address": item.get("address"),
                        "area": item.get("area"),
                        "pincode": item.get("pincode"),
                        "contact_number": item.get("contact_number"),
                        "email": item.get("email"),
                        "active": item.get("active", True),
                    }
                    for item in data
                ]
                return Response(formatted_data, status=status.HTTP_200_OK)

            except requests.RequestException as e:
                return Response(
                    {"error": f"Failed to fetch external API: {e}"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

        queryset = self.get_queryset().order_by("id")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        center = serializer.save(created_by=request.user, updated_by=request.user)
        return Response(
            {
                "message": "Diagnostic center created successfully",
                "data": self.get_serializer(center).data
            },
            status=status.HTTP_201_CREATED
        )
        
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "message": "Diagnostic center updated successfully",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response(
            {
                "message": "Diagnostic center partially updated successfully",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {
                "message": "Diagnostic center deleted successfully"
            },
            status=status.HTTP_200_OK
        )

class DiagnosticCenterSearchAPIView(APIView):

    VALID_KEYS = {
        "city_id",
        "test_ids",
        "health_package_id",
        "sponsored_package_id"
    }

    def post(self, request):

        # validate keys
        received_keys = set(request.data.keys())
        invalid_keys = received_keys - self.VALID_KEYS

        if invalid_keys:
            suggestions = {}
            for invalid in invalid_keys:
                close = self.get_close_key(invalid)
                if close:
                    suggestions[invalid] = f"Did you mean '{close}'?"

            response = {
                "detail": f"Invalid parameters: {', '.join(invalid_keys)}"
            }
            if suggestions:
                response["suggestions"] = suggestions

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        city_id = request.data.get("city_id")
        test_ids = request.data.get("test_ids", [])
        health_package_id = request.data.get("health_package_id")
        sponsored_package_id = request.data.get("sponsored_package_id")

        if not city_id:
            return Response({"detail": "City is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            return Response({"detail": "City not found."}, status=status.HTTP_404_NOT_FOUND)

        diagnostic_centers = DiagnosticCenter.objects.filter(city=city).distinct()

        if health_package_id:
            diagnostic_centers = diagnostic_centers.filter(health_packages__id=health_package_id)

        if sponsored_package_id:
            diagnostic_centers = diagnostic_centers.filter(sponsored_packages__id=sponsored_package_id)

        if test_ids:
            test_ids = [int(tid) for tid in test_ids if str(tid).isdigit()]
            diagnostic_centers = diagnostic_centers.filter(tests__in=test_ids).distinct()
            diagnostic_centers = [
                dc for dc in diagnostic_centers
                if set(test_ids).issubset(set(dc.tests.values_list("id", flat=True)))
            ]

        if not diagnostic_centers:
            return Response(
                {"detail": "No diagnostic centers found for the selected filters."},
                status=status.HTTP_200_OK
            )

        # serializer = DiagnosticCenterSerializer(diagnostic_centers, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        if hasattr(diagnostic_centers, "values"):
            centers = list(diagnostic_centers.values("id", "name"))
        else:
            centers = [{"id": dc.id, "name": dc.name} for dc in diagnostic_centers]

        return Response({"centers": centers}, status=status.HTTP_200_OK)

    def get_close_key(self, invalid_key):
        from difflib import get_close_matches
        matches = get_close_matches(invalid_key, self.VALID_KEYS, n=1, cutoff=0.6)
        return matches[0] if matches else None
