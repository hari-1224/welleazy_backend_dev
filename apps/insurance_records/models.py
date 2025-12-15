from django.db import models
from django.conf import settings

from apps.common.models import BaseModel
from apps.dependants.models import Dependant


class InsurancePolicyRecord(BaseModel):

    POLICY_OWNER_CHOICES = (
        ("company", "Company Policy"),
        ("self", "Self"),
        ("dependant", "Dependent"),
    )

    FOR_WHOM_CHOICES = (
        ("self", "Self"),
        ("dependant", "Dependant"),
    )

    PLAN_TYPE_CHOICES = (
        ("individual", "Individual"),
        ("floater", "Floater"),
    )

    TYPE_OF_INSURANCE_CHOICES = (
        ("health", "Health Insurance"),
        ("life", "Life Insurance"),
        ("personal_accident", "Personal Accident"),
        ("critical_illness", "Critical Illness"),
        ("other", "Other"),
    )

    RENEWAL_FREQUENCY_CHOICES = (
        ("one_time", "One time"),
        ("recurring", "Recurring"),
    )

    REMINDER_TYPE_CHOICES = (
        ("days", "Days"),
        ("two_weeks", "2 Week"),
        ("one_week", "1 Week"),
        ("one_month", "1 Month"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="insurance_policies",
    )

    # tab type
    policy_owner_type = models.CharField(
        max_length=20,
        choices=POLICY_OWNER_CHOICES,
        default="self",
    )

    # individual mode (like other health records)
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
        related_name="individual_insurance_policies",
    )

    # floater mode
    plan_type = models.CharField(
        max_length=20,
        choices=PLAN_TYPE_CHOICES,
        default="individual",
    )
    is_self_included = models.BooleanField(default=True)

    # main policy fields
    policy_holder_name = models.CharField(max_length=255)
    policy_from = models.DateField()
    policy_to = models.DateField()

    type_of_insurance = models.CharField(
        max_length=50,
        choices=TYPE_OF_INSURANCE_CHOICES,
    )
    insurance_company = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=100)
    policy_name = models.CharField(max_length=255)

    sum_assured = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    premium_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    tpa = models.CharField(max_length=255, blank=True, null=True)
    nominee = models.CharField(max_length=255, blank=True, null=True)

    # renewal reminder popup
    renewal_reminder_enabled = models.BooleanField(default=False)
    renewal_frequency = models.CharField(
        max_length=20,
        choices=RENEWAL_FREQUENCY_CHOICES,
        blank=True,
        null=True,
    )
    renewal_reminder_type = models.CharField(
        max_length=20,
        choices=REMINDER_TYPE_CHOICES,
        blank=True,
        null=True,
    )
    renewal_reminder_value = models.PositiveIntegerField(
        default=1,
        help_text="Number of days/weeks/months before policy_to date.",
    )

    # right side details
    group_policy_details = models.TextField(blank=True, null=True)
    policy_features = models.TextField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.policy_holder_name} - {self.policy_name} ({self.policy_number})"


class InsuranceFloaterMember(BaseModel):

    policy = models.ForeignKey(
        InsurancePolicyRecord,
        on_delete=models.CASCADE,
        related_name="floater_members",
    )
    dependant = models.ForeignKey(
        Dependant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="floater_entries",
    )
    is_self = models.BooleanField(default=False)
    uhid = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        if self.is_self:
            return f"Self – UHID: {self.uhid}"
        if self.dependant:
            return f"{self.dependant.name} – UHID: {self.uhid}"
        return f"Floater member (policy {self.policy_id})"


class InsurancePolicyDocument(BaseModel):

    policy = models.ForeignKey(
        InsurancePolicyRecord,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    file = models.FileField(upload_to="insurance_records/")

    def __str__(self):
        return f"Document for {self.policy}"
