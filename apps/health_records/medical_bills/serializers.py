from rest_framework import serializers
from .models import MedicalBillRecord, MedicalBillDocument
from apps.dependants.serializers import DependantSerializer
from rest_framework.exceptions import ValidationError
from apps.common.serializers.dependant_mixin import DependantResolverMixin

class MedicalBillDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalBillDocument
        exclude = ("created_by", "updated_by", "deleted_at")


class MedicalBillRecordSerializer(DependantResolverMixin, serializers.ModelSerializer):

    documents = MedicalBillDocumentSerializer(many=True, read_only=True)
    # dependant_data = DependantSerializer(source="dependant", read_only=True)
    bill_type = serializers.SerializerMethodField()

    class Meta:
        model = MedicalBillRecord
        fields = [
            "id", "for_whom", "dependant", "dependant_data",
            "bill_type", "record_name", "record_date",
            "record_bill_number", "record_hospital_name",
            "notes", "documents",
            "created_at", "updated_at", "created_by", "updated_by"
        ]

    def get_bill_type(self, obj):
        return obj.get_bill_type_display()


class MedicalBillPayloadSerializer(serializers.Serializer):
    record_id = serializers.IntegerField(required=False)

    record_name = serializers.CharField()
    record_date = serializers.DateField()
    record_bill_number = serializers.CharField()
    record_hospital_name = serializers.CharField()

    bill_type = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)

    for_whom = serializers.ChoiceField(
        choices=MedicalBillRecord.FOR_WHOM_CHOICES,
        required=False,
        default="self"
    )
    dependant = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        for_whom = data.get("for_whom", "self")
        dependant = data.get("dependant")

        if for_whom == "dependant" and dependant is None:
            raise ValidationError({
                "dependant": "Dependants must be provided when for_whom is 'dependant'."
            })

        if for_whom == "self":
            data["dependant"] = None

        return data
