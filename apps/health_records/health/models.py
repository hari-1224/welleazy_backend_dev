from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class HeightRecord(BaseModel):
    UNIT_CHOICES = (
        ("cm", "Centimeters"),
        ("ft", "Feet"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="height_records"
    )
    value = models.FloatField()
    unit = models.CharField(max_length=5)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Height Record"
        verbose_name_plural = "Height Records"

    def __str__(self):
        return f"{self.user} - {self.value} {self.unit}"

class WeightRecord(BaseModel):
    UNIT_CHOICES = (
        ("kg", "Kilograms"),
        ("lb", "Pounds"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="weight_records"
    )
    value = models.FloatField()
    unit = models.CharField(max_length=5)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Weight Record"
        verbose_name_plural = "Weight Records"

    def __str__(self):
        return f"{self.user} - {self.value} {self.unit}"
    
class BmiRecord(BaseModel):
    UNIT_CHOICES = (
        ("BMI", "Body Mass Index"),
        ("kg/m²", "Kilograms per square meter"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bmi_records"
    )
    value = models.FloatField(help_text="Body Mass Index value")
    unit = models.CharField(max_length=10)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "BMI Record"
        verbose_name_plural = "BMI Records"

    def __str__(self):
        return f"{self.user} - {self.value} {self.unit}"
    
class BloodPressureRecord(BaseModel):
    TYPE_CHOICES = (
        ("normal", "Normal"),
        ("exercise", "Exercise"),
        ("rest", "Rest"),
        ("other", "Other"),
    )

    UNIT_CHOICES = (
        ("mmHg", "MMHG"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blood_pressure_records"
    )
    systolic = models.PositiveIntegerField(help_text="Systolic pressure (upper value)")
    diastolic = models.PositiveIntegerField(help_text="Diastolic pressure (lower value)")
    unit = models.CharField(max_length=10)
    type = models.CharField(max_length=20)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Blood Pressure Record"
        verbose_name_plural = "Blood Pressure Records"

    def __str__(self):
        return f"{self.user} - {self.systolic}/{self.diastolic} {self.unit}"

    @property
    def category(self):
        if self.systolic < 90 or self.diastolic < 60:
            return "Low"
        elif 90 <= self.systolic < 120 and 60 <= self.diastolic < 80:
            return "Normal"
        elif 120 <= self.systolic < 130 and self.diastolic < 80:
            return "Elevated"
        elif 130 <= self.systolic < 140 or 80 <= self.diastolic < 90:
            return "Hypertension Stage 1"
        elif 140 <= self.systolic < 180 or 90 <= self.diastolic < 120:
            return "Hypertension Stage 2"
        else:
            return "Hypertensive Crisis"
        
class HeartRateRecord(BaseModel):
    UNIT_CHOICES = (
        ("bpm", "Beats Per Minute"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="heart_rate_records"
    )
    value = models.PositiveIntegerField()
    unit = models.CharField(max_length=10)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Heart Rate Record"
        verbose_name_plural = "Heart Rate Records"

    def __str__(self):
        return f"{self.user} - {self.value} {self.unit}"
    
class OxygenSaturationRecord(BaseModel):
    UNIT_CHOICES = (
        ("%", "Percentage"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="oxygen_saturation_records"
    )
    value = models.FloatField(help_text="Oxygen saturation percentage")
    unit = models.CharField(max_length=5)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Oxygen Saturation Record"
        verbose_name_plural = "Oxygen Saturation Records"

    def __str__(self):
        return f"{self.user} - {self.value}{self.unit}"
    
class GlucoseRecord(BaseModel):
    UNIT_CHOICES = (
        ("mg/dL", "Milligrams per Deciliter"),
        ("mmol/l", "Millimoles per Liter"),
    )

    TYPE_CHOICES = (
        ("fasting", "Fasting"),
        ("postprandial", "Postprandial (After Meal)"),
        ("random", "Random"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="glucose_records"
    )
    value = models.FloatField(help_text="Blood glucose value")
    unit = models.CharField(max_length=10)
    test_type = models.CharField(max_length=20)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Glucose Record"
        verbose_name_plural = "Glucose Records"

    def __str__(self):
        return f"{self.user} - {self.value} {self.unit} ({self.test_type})"