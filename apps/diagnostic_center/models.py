from django.db import models
from apps.common.models import BaseModel
from apps.location.models import City
from apps.labtest.models import Test
from apps.labfilter.models import VisitType
from datetime import time

class DiagnosticCenter(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    active = models.BooleanField(default=True)
    work_start = models.TimeField(default=time(8, 0))   # 8 AM
    work_end = models.TimeField(default=time(20, 0))     # 8 PM

    slot_interval_minutes = models.IntegerField(default=30)  # 30 min slot
    slot_capacity = models.IntegerField(default=1)           # 1 person per slot

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="diagnostic_centers")
    tests = models.ManyToManyField(Test, related_name="diagnostic_centers")
    visit_types = models.ManyToManyField(VisitType, related_name="diagnostic_centers", blank=True)

    health_packages = models.ManyToManyField(
        'health_packages.HealthPackage', related_name='diagnostic_centers', blank=True
    )
    sponsored_packages = models.ManyToManyField(
        'sponsored_packages.SponsoredPackage', related_name='diagnostic_centers', blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.code or 'N/A'})"
