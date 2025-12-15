from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from apps.consultation_filter.models import Vendor

User = settings.AUTH_USER_MODEL


# ---------------------------------------
#  EYE TREATMENTS
# ---------------------------------------
class EyeTreatment(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(blank=True)
    detailed_description = models.TextField(blank=True)
    image = models.ImageField(upload_to="eye_treatments/", blank=True, null=True)

    def __str__(self):
        return self.name


# ---------------------------------------
#  DENTAL TREATMENTS
# ---------------------------------------
class DentalTreatment(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(blank=True)
    detailed_description = models.TextField(blank=True)
    image = models.ImageField(upload_to="dental_treatments/", blank=True, null=True)

    def __str__(self):
        return self.name




class EyeVendorAddress(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="eye_addresses")
    address = models.TextField()
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.vendor.name} - {self.address}"


class DentalVendorAddress(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="dental_addresses")
    address = models.TextField()
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.vendor.name} - {self.address}"




class EyeDentalVoucher(models.Model):

    SERVICE_TYPE = [
        ("eye", "Eye Care"),
        ("dental", "Dental Care"),
    ]

    BOOKING_FOR = [
        ("self", "Self"),
        ("dependant", "Dependant"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_id = models.CharField(max_length=20, unique=True, editable=False)

    user = models.ForeignKey(User , on_delete=models.CASCADE)

    booking_for = models.CharField(max_length=20, choices=BOOKING_FOR, default="self")
    dependant_name = models.CharField(max_length=255, blank=True, null=True)
    dependant_relationship = models.CharField(max_length=255, blank=True, null=True)

    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE)

    # Treatments
    eye_treatment = models.ForeignKey(EyeTreatment, null=True, blank=True, on_delete=models.SET_NULL)
    dental_treatment = models.ForeignKey(DentalTreatment, null=True, blank=True, on_delete=models.SET_NULL)

    # Vendors
    eye_vendor = models.ForeignKey(EyeVendorAddress, null=True, blank=True, on_delete=models.SET_NULL)
    dental_vendor = models.ForeignKey(DentalVendorAddress, null=True, blank=True, on_delete=models.SET_NULL)

    # User / dependant details
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.request_id:
            last_id = EyeDentalVoucher.objects.count() + 1
            self.request_id = f"WX{last_id:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.request_id


