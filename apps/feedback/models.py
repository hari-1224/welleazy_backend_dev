from django.db import models
from django.conf import settings
from apps.common.models import BaseModel


class SiteFeedback(BaseModel):

    SATISFACTION_CHOICES = (
        ("satisfied", "Satisfied"),
        ("neutral", "Neutral"),
        ("unsatisfied", "Unsatisfied"),
    )

    TIMELY_CHOICES = (
        ("yes", "Yes"),
        ("no", "No"),
    )

    PROFESSIONALISM_CHOICES = (
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("average", "Average"),
        ("poor", "Poor"),
        ("very_poor", "Very Poor"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="site_feedback",
        null=True, blank=True
    )

    satisfaction = models.CharField(max_length=20, choices=SATISFACTION_CHOICES)
    timely_service = models.CharField(max_length=10, choices=TIMELY_CHOICES)
    professionalism = models.CharField(max_length=20, choices=PROFESSIONALISM_CHOICES)

    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Website Feedback ({self.id})"
