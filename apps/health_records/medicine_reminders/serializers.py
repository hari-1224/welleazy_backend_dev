from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import MedicineReminder, MedicineReminderTime, MedicineReminderDocument


class MedicineReminderDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineReminderDocument
        exclude = ("created_by", "updated_by", "deleted_at")


class MedicineReminderTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineReminderTime
        fields = ["id", "time", "meal_relation"]


class MedicineReminderSerializer(serializers.ModelSerializer):
    schedule_times = MedicineReminderTimeSerializer(many=True, read_only=True)
    documents = MedicineReminderDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = MedicineReminder
        fields = [
            "id",
            "medicine_name",
            "medicine_type",

            "duration_value",
            "duration_unit",
            "start_date",
            "end_date",

            "frequency_type",
            "intake_frequency",
            "interval_type",
            "interval_start_time",
            "interval_end_time",

            "dosage_value",
            "dosage_unit",
            "doctor_name",
            "appointment_reminder_date",

            "current_inventory",
            "remind_when_inventory",
            "medicines_left",

            "schedule_times",
            "documents",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = ("created_at", "updated_at", "created_by", "updated_by")


class MedicineReminderTimeInputSerializer(serializers.Serializer):
    time = serializers.TimeField(format="%H:%M", input_formats=["%H:%M"])
    meal_relation = serializers.ChoiceField(
        choices=MedicineReminder.MEAL_RELATION_CHOICES
    )


class MedicineReminderPayloadSerializer(serializers.Serializer):
    # same as before...
    medicine_name = serializers.CharField()
    medicine_type = serializers.ChoiceField(
        choices=MedicineReminder.MEDICINE_TYPE_CHOICES
    )

    duration_value = serializers.IntegerField(min_value=1)
    duration_unit = serializers.ChoiceField(
        choices=MedicineReminder.DURATION_UNIT_CHOICES, default="day"
    )

    start_date = serializers.DateField()
    end_date = serializers.DateField()

    frequency_type = serializers.ChoiceField(
        choices=MedicineReminder.FREQUENCY_TYPE_CHOICES
    )

    intake_frequency = serializers.ChoiceField(
        choices=MedicineReminder.INTAKE_FREQUENCY_CHOICES,
        required=False,
        allow_null=True,
    )
    schedule_times = MedicineReminderTimeInputSerializer(
        many=True, required=False
    )

    interval_type = serializers.ChoiceField(
        choices=MedicineReminder.INTERVAL_TYPE_CHOICES,
        required=False,
        allow_null=True,
    )
    interval_start_time = serializers.TimeField(
        required=False, allow_null=True,
        format="%H:%M", input_formats=["%H:%M"]
    )
    interval_end_time = serializers.TimeField(
        required=False, allow_null=True,
        format="%H:%M", input_formats=["%H:%M"]
    )

    dosage_value = serializers.IntegerField(min_value=1)
    dosage_unit = serializers.ChoiceField(
        choices=MedicineReminder.DOSAGE_UNIT_CHOICES
    )

    doctor_name = serializers.CharField(required=False, allow_blank=True)
    appointment_reminder_date = serializers.DateField(
        required=False, allow_null=True
    )

    current_inventory = serializers.IntegerField(min_value=0, required=False)
    remind_when_inventory = serializers.IntegerField(min_value=0, required=False)
    medicines_left = serializers.IntegerField(min_value=0, required=False)

    def validate(self, data):
        # same validation as before...
        freq_type = data.get("frequency_type")

        if data["end_date"] < data["start_date"]:
            raise ValidationError({"end_date": "End date cannot be before start date."})

        if freq_type == "fixed_times":
            if not data.get("intake_frequency"):
                raise ValidationError({
                    "intake_frequency": "Required when frequency_type is 'fixed_times'."
                })
            times = data.get("schedule_times") or []
            if not times:
                raise ValidationError({
                    "schedule_times": "At least one scheduled time is required."
                })
            for f in ("interval_type", "interval_start_time", "interval_end_time"):
                if data.get(f) is not None:
                    raise ValidationError({
                        f: f"Should be empty when frequency_type is 'fixed_times'."
                    })

        elif freq_type == "interval":
            if not data.get("interval_type"):
                raise ValidationError({
                    "interval_type": "Required when frequency_type is 'interval'."
                })
            if not data.get("interval_start_time") or not data.get("interval_end_time"):
                raise ValidationError({
                    "interval_start_time": "Start and end time are required for interval mode.",
                    "interval_end_time": "Start and end time are required for interval mode.",
                })
            if data["interval_end_time"] <= data["interval_start_time"]:
                raise ValidationError({
                    "interval_end_time": "End time must be after start time."
                })
            if data.get("intake_frequency"):
                raise ValidationError({
                    "intake_frequency": "Must be empty when frequency_type is 'interval'."
                })
            if data.get("schedule_times"):
                raise ValidationError({
                    "schedule_times": "Must be empty when frequency_type is 'interval'."
                })

        data.setdefault("current_inventory", 0)
        data.setdefault("remind_when_inventory", 0)
        data.setdefault("medicines_left", data["current_inventory"])

        return data
