# apps/care_programs/models.py
from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
from apps.dependants.models import Dependant
from apps.addresses.models import Address
from apps.location.models import State, City

User = settings.AUTH_USER_MODEL


class CareProgramBooking(BaseModel):
    FOR_WHOM_CHOICES = [
        ("self", "Self"),
        ("dependant", "Dependant"),
    ]

    SERVICE_TYPE_CHOICES = [
        ("elderly_care_attendance", "Elderly Care Attendance"),
        ("elderly_care_program", "Elderly Care Program"),
        ("home_nursing", "Home Nursing"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
        ("callback_requested", "Callback Requested"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="care_program_bookings",
    )

    for_whom = models.CharField(
        max_length=20,
        choices=FOR_WHOM_CHOICES,
        default="self",
    )

    dependant = models.ForeignKey(
        Dependant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="care_program_bookings",
    )

    name = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()

    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="care_program_bookings",
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="care_program_bookings",
    )
    address_text = models.TextField()

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="care_program_bookings",
    )

    service_type = models.CharField(
        max_length=100,
        choices=SERVICE_TYPE_CHOICES,
    )

    requirements = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service_type} booking for {self.name} ({self.status})"
