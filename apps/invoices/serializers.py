from rest_framework import serializers
from .models import AppointmentInvoice

class AppointmentInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentInvoice
        fields = "__all__"
