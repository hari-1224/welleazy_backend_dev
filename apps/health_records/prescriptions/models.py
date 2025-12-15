from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
from apps.dependants.models import Dependant
from apps.consultation_filter.models import DoctorSpeciality


class PrescriptionRecord(BaseModel):

    PRESCRIPTION_TYPE_CHOICES = (
        ("health_record", "Health Record"),
        ("radiology_report", "Radiology Medical Report"),
        ("lab_report", "Lab Report"),
        ("doctor_prescription", "Doctor Prescription"),
    )

    FOR_WHOM_CHOICES = (
        ("self", "Self"),
        ("dependant", "Dependant"),
    )   

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="prescription_records"
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

    record_type = models.CharField(max_length=50, choices=PRESCRIPTION_TYPE_CHOICES)
    record_name = models.CharField(max_length=255)

    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    doctor_specialization = models.ForeignKey(
        DoctorSpeciality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    record_date = models.DateField()
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.record_name} ({self.get_record_type_display()})"


class PrescriptionParameter(BaseModel):
    record = models.ForeignKey(
        PrescriptionRecord, on_delete=models.CASCADE, related_name="parameters"
    )
    parameter_name = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    start_range = models.CharField(max_length=50, blank=True, null=True)
    end_range = models.CharField(max_length=50, blank=True, null=True)


class PrescriptionDocument(BaseModel):
    record = models.ForeignKey(
        PrescriptionRecord, on_delete=models.CASCADE, related_name="documents"
    )
    file = models.FileField(upload_to="health_records/")
