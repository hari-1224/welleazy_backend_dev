from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
from apps.dependants.models import Dependant


class HospitalizationRecord(BaseModel):

    HOSPITALIZATION_TYPE_CHOICES = (
        ("inpatient", "Inpatient"),
        ("outpatient", "Outpatient"),
        ("emergency", "Emergency"),
        ("surgery", "Surgery"),
    )

    FOR_WHOM_CHOICES = (
        ("self", "Self"),
        ("dependant", "Dependant"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hospitalization_records"
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

    hospitalization_type = models.CharField(max_length=50, choices=HOSPITALIZATION_TYPE_CHOICES)

    record_name = models.CharField(max_length=255)
    hospital_name = models.CharField(max_length=255)
    admitted_date = models.DateField()
    discharged_date = models.DateField(null=True, blank=True)

    doctor_name = models.CharField(max_length=255, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.record_name} ({self.get_hospitalization_type_display()})"


class HospitalizationDocument(BaseModel):
    record = models.ForeignKey(
        HospitalizationRecord, on_delete=models.CASCADE, related_name="documents"
    )
    file = models.FileField(upload_to="hospitalizations/")
