from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import VaccinationCertificateRecord, VaccinationCertificateDocument
from apps.dependants.serializers import DependantSerializer
from apps.common.serializers.dependant_mixin import DependantResolverMixin


class VaccinationCertificateDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccinationCertificateDocument
        exclude = ("created_by", "updated_by", "deleted_at")


class VaccinationCertificateRecordSerializer(DependantResolverMixin, serializers.ModelSerializer):

    documents = VaccinationCertificateDocumentSerializer(many=True, read_only=True)
    # dependant_data = DependantSerializer(source="dependant", read_only=True)

    class Meta:
        model = VaccinationCertificateRecord
        fields = [
            "id",
            "for_whom", "dependant", "dependant_data", "patient_name",

            "vaccination_date",
            "vaccination_name",
            "vaccination_dose",
            "vaccination_center",
            "registration_id",

            "notes",
            "documents",
            "created_at", "updated_at",
            "created_by", "updated_by",
        ]


class VaccinationPayloadSerializer(serializers.Serializer):
    record_id = serializers.IntegerField(required=False)

    vaccination_date = serializers.DateField()
    vaccination_name = serializers.CharField()
    vaccination_dose = serializers.CharField()
    vaccination_center = serializers.CharField()
    registration_id = serializers.CharField(required=False, allow_blank=True)

    notes = serializers.CharField(required=False, allow_blank=True)

    for_whom = serializers.ChoiceField(
        choices=VaccinationCertificateRecord.FOR_WHOM_CHOICES,
        required=False,
        default="self"
    )
    dependant = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        for_whom = data.get("for_whom", "self")
        dependant = data.get("dependant")

        if for_whom == "dependant" and dependant is None:
            raise ValidationError({"dependant": "Dependants must be provided when for_whom is 'dependant'."})

        if for_whom == "self":
            data["dependant"] = None

        return data
