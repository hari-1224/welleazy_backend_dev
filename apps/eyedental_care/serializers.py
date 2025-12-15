from rest_framework import serializers
from .models import EyeTreatment, DentalTreatment, EyeVendorAddress , DentalVendorAddress , EyeDentalVoucher
from apps.dependants.models import Dependant

from apps.consultation_filter.models import DoctorSpeciality
from apps.appointments.models import CartItem


class EyeTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EyeTreatment
        fields = "__all__"


class DentalTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalTreatment
        fields = "__all__"


class EyeVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EyeVendorAddress
        fields = "__all__"


class DentalVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model= DentalVendorAddress
        fields= "__all__"





class EyeDentalVoucherCreateSerializer(serializers.ModelSerializer):
    dependant_id = serializers.IntegerField(required=False)


    class Meta:
        model = EyeDentalVoucher
        fields = [
            "booking_for",
            "service_type",

            "eye_treatment",
            "dental_treatment",

            "eye_vendor",
            "dental_vendor",

            "name",
            "dependant_relationship",
            "contact_number",
            "email",
            "state",
            "city",
            "address",
            "dependant_id"
        ]

    def validate(self, data):
        service_type = data.get("service_type")

        # Validate for EYE CARE
        if service_type == "eye":
            if not data.get("eye_treatment"):
                raise serializers.ValidationError("eye_treatment is required for Eye Care.")
            if not data.get("eye_vendor"):
                raise serializers.ValidationError("eye_vendor is required for Eye Care.")

        # Validate for DENTAL CARE
        if service_type == "dental":
            if not data.get("dental_treatment"):
                raise serializers.ValidationError("dental_treatment is required for Dental Care.")
            if not data.get("dental_vendor"):
                raise serializers.ValidationError("dental_vendor is required for Dental Care.")

        return data

   
    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        dependant_name = None
        dependant_relationship = None

        if validated_data.get("booking_for") == "dependant":
            dep_id = validated_data.pop("dependant_id")
            dependant_obj = Dependant.objects.get(id=dep_id, user=user)
            dependant_name = dependant_obj.name
            dependant_relationship = dependant_obj.relationship

        voucher = EyeDentalVoucher.objects.create(
            user=user,
            booking_for=validated_data.get("booking_for"),

            dependant_name=dependant_name,
            dependant_relationship=dependant_relationship,

            service_type=validated_data.get("service_type"),

            eye_treatment=validated_data.get("eye_treatment"),
            dental_treatment=validated_data.get("dental_treatment"),

            eye_vendor=validated_data.get("eye_vendor"),
            dental_vendor=validated_data.get("dental_vendor"),

            name=validated_data.get("name"),
            contact_number=validated_data.get("contact_number"),
            email=validated_data.get("email"),
            state=validated_data.get("state"),
            city=validated_data.get("city"),
            address=validated_data.get("address"),
    )

        return voucher


class EyeDentalVoucherSerializer(serializers.ModelSerializer):

    request_id = serializers.CharField(read_only=True)
    service_name = serializers.SerializerMethodField()
    treatment_name = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()
    center_address = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()  # self or dependant

    class Meta:
        model = EyeDentalVoucher
        fields = [
            "request_id",
            "name",
            "vendor_name",
            "center_address",
            "service_name",
            "treatment_name",
            "created_at",
           
        ]

    def get_name(self, obj):
        if obj.booking_for == "dependant":
            return obj.dependant_name
        user=obj.user
        return user.name
    
     

    def get_vendor_name(self, obj):
        if obj.service_type == "eye" and obj.eye_vendor:
            return obj.eye_vendor.vendor.name
        if obj.service_type == "dental" and obj.dental_vendor:
            return obj.dental_vendor.vendor.name
        return None

    def get_center_address(self, obj):
        if obj.service_type == "eye" and obj.eye_vendor:
            return obj.eye_vendor.address
        if obj.service_type == "dental" and obj.dental_vendor:
            return obj.dental_vendor.address
        return None

    def get_service_name(self, obj):
        return "Eye Care" if obj.service_type == "eye" else "Dental Care"

    def get_treatment_name(self, obj):
        if obj.service_type == "eye" and obj.eye_treatment:
            return obj.eye_treatment.name
        if obj.service_type == "dental" and obj.dental_treatment:
            return obj.dental_treatment.name
        return None

