from rest_framework import serializers
from .models import SiteFeedback


class SiteFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteFeedback
        fields = [
            "id",
            "satisfaction",
            "timely_service",
            "professionalism",
            "remarks",
            "created_at",
        ]
        read_only_fields = ("created_at",)
