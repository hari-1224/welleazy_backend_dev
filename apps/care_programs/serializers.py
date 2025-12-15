# apps/care_programs/serializers.py
from rest_framework import serializers
from .models import CareProgramBooking


class CareProgramBookingSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source="state.name", read_only=True)
    city_name = serializers.CharField(source="city.name", read_only=True)
    address_type_name = serializers.CharField(
        source="address.address_type.name",
        read_only=True,
    )

    class Meta:
        model = CareProgramBooking
        fields = "__all__"
        read_only_fields = (
            "user",
            "name",
            "email",
            "contact_number",
            "state",
            "city",
            "address_text",
            "address",
            "status",
            "created_at",
            "updated_at",
        )


class CareProgramBookingPayloadSerializer(serializers.Serializer):
    for_whom = serializers.ChoiceField(choices=["self", "dependant"])
    service_type = serializers.ChoiceField(
        choices=[c[0] for c in CareProgramBooking.SERVICE_TYPE_CHOICES]
    )
    requirements = serializers.CharField(required=False, allow_blank=True)

    dependant = serializers.IntegerField(required=False, allow_null=True)


    address = serializers.IntegerField(required=False, allow_null=True)
    state = serializers.IntegerField(required=False, allow_null=True)
    city = serializers.IntegerField(required=False, allow_null=True)
    address_text = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if data["for_whom"] == "dependant" and not data.get("dependant"):
            raise serializers.ValidationError(
                {"dependant": "Dependant is required when for_whom='dependant'."}
            )

        if data["for_whom"] == "self":
            data["dependant"] = None


        return data
