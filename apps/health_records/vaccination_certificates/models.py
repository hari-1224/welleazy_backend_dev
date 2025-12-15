from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
from apps.dependants.models import Dependant


class VaccinationCertificateRecord(BaseModel):
    
    VACCINE_TYPE_CHOICES = (
        ("covid", "COVID-19 Vaccine"),
        ("hepatitis_b", "Hepatitis B"),
        ("mmr", "MMR - Measles, Mumps, Rubella"),
        ("tetanus", "Tetanus (TT/DT)"),
        ("typhoid", "Typhoid Vaccine"),
        ("influenza", "Influenza Vaccine"),
        ("other", "Other"),
    )
    FOR_WHOM_CHOICES = (
        ("self", "Self"),
        ("dependant", "Dependant"),
    )

    for_whom = models.CharField(
        max_length=20,
        choices=FOR_WHOM_CHOICES,
        default="self",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    dependant = models.ForeignKey(
        Dependant, on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # EXACT UI fields:
    vaccination_date = models.DateField()
    vaccination_name = models.CharField(max_length=255)
    vaccination_dose = models.CharField(max_length=50)
    vaccination_center = models.CharField(max_length=255)
    registration_id = models.CharField(max_length=255, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.vaccination_name} - {self.vaccination_dose}"

class VaccinationCertificateDocument(BaseModel):
    record = models.ForeignKey(
        VaccinationCertificateRecord,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    file = models.FileField(upload_to="vaccination_certificates/")