from rest_framework import serializers
from apps.diagnostic_center.models import DiagnosticCenter
from apps.location.models import City
from apps.location.serializers import CitySerializer
from apps.labtest.models import Test
from apps.labtest.serializers import TestSerializer
from apps.labfilter.models import VisitType
from apps.labfilter.serializers import VisitTypeSerializer
from apps.health_packages.models import HealthPackage
from apps.sponsored_packages.models import SponsoredPackage
from apps.health_packages.serializers import HealthPackageSerializer
from apps.sponsored_packages.serializers import SponsoredPackageSerializer


class DiagnosticCenterSerializer(serializers.ModelSerializer):
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        source='city',
        write_only=True
    )
    city = CitySerializer(read_only=True)

    test_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Test.objects.all(),
        source='tests',
        write_only=True
    )

    tests = TestSerializer(read_only=True, many=True)

    visit_type_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=VisitType.objects.all(),
        source='visit_types',
        write_only=True
    )
    visit_types = VisitTypeSerializer(read_only=True, many=True)

    health_package_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=HealthPackage.objects.all(),
        source='health_packages',
        write_only=True,
        required=False
    )
    sponsored_package_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SponsoredPackage.objects.all(),
        source='sponsored_packages',
        write_only=True,
        required=False
    )

    health_packages = HealthPackageSerializer(read_only=True, many=True)
    sponsored_packages = SponsoredPackageSerializer(read_only=True, many=True)

    class Meta:
        model = DiagnosticCenter
        fields = [
            'id', 'name', 'code', 'address', 'area', 'pincode',
            'contact_number', 'email', 'active',
            'city', 'city_id',
            'tests', 'test_ids',
            'visit_types', 'visit_type_ids',
            'health_packages', 'sponsored_packages',
            'health_package_ids', 'sponsored_package_ids',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)

    #     mode = self.context.get("mode")
    #     if mode == "cart":
    #         data.pop("tests", None)
    #         data.pop("health_packages", None)
    #         data.pop("sponsored_packages", None)
    #         data.pop("visit_types", None)

    #     return data