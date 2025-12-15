from rest_framework import serializers
from .models import DoctorPersonalDetails,DoctorProfessionalDetails
from apps.consultation_filter.serializers import VendorSerializer, LanguageSerializer , DoctorSpecialitySerializer
from apps.consultation_filter.models import Vendor,Language,DoctorSpeciality

class DoctorPersonalDetailsSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = DoctorPersonalDetails
        fields = [
            "id", "full_name", "gender", "dob","age","blood_group",
            "phone", "email", "address", "profile_photo" 
        ]




class DoctorProfessionalDetailsSerializer(serializers.ModelSerializer):

    # Read only
    specialization = DoctorSpecialitySerializer(read_only=True)
    vendor = VendorSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    name = serializers.CharField(source="doctor.full_name", read_only=True)

    # Write only
    specialization_id = serializers.PrimaryKeyRelatedField(
        queryset=DoctorSpeciality.objects.all(),
        source="specialization",
        write_only=True
    )
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(),
        source="vendor",
        write_only=True
    )
    language_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(),
        source="language",
        write_only=True
    )

    class Meta:
        model = DoctorProfessionalDetails
        fields = [
            "id",
            "doctor",
            "name",
            "vendor", "vendor_id",
            "specialization", "specialization_id",
            "language", "language_id",
            "experience_years",
            "consultation_fee",
            "license_number",
            "clinic_address",
            "e_consultation",
            "in_clinic",
        ]