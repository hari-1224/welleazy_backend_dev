from rest_framework import serializers
from .models import SponsoredPackage
from apps.labtest.models import Test
from apps.labtest.serializers import TestSerializer

class SponsoredPackageSerializer(serializers.ModelSerializer):
    test_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Test.objects.all(),
        source='tests',
        write_only=True
    )
    tests = TestSerializer(read_only=True, many=True)

    class Meta:
        model = SponsoredPackage
        fields = [
            'id', 'name', 'code', 'description', 'price', 'validity_till',
            'active', 'tests', 'test_ids', 'created_at', 'updated_at', 'status',
        ]
        read_only_fields = ['created_at', 'updated_at']
