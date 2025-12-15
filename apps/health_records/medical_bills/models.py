from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
from apps.dependants.models import Dependant


class MedicalBillRecord(BaseModel):

    MEDICAL_BILL_TYPE_CHOICES = (
        ("consultation", "Consultation Bill"),
        ("pharmacy", "Pharmacy Bill"),
        ("diagnostic", "Diagnostic Bill"),
        ("hospital", "Hospital Bill"),
        ("other", "Other"),
    )

    FOR_WHOM_CHOICES = (
        ("self", "Self"),
        ("dependant", "Dependant"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medical_bill_records"
    )

    for_whom = models.CharField(
        max_length=20,
        choices=FOR_WHOM_CHOICES,
        default="self",
    )

    dependant = models.ForeignKey(
        Dependant, on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # bill fields
    record_name = models.CharField(max_length=255)
    record_date = models.DateField()
    record_bill_number = models.CharField(max_length=255)
    record_hospital_name = models.CharField(max_length=255)

    bill_type = models.CharField(max_length=30, choices=MEDICAL_BILL_TYPE_CHOICES)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.record_name} ({self.get_bill_type_display()})"


class MedicalBillDocument(BaseModel):
    record = models.ForeignKey(
        MedicalBillRecord, on_delete=models.CASCADE, related_name="documents"
    )
    file = models.FileField(upload_to="medical_bills/")
