from django.db import models
from apps.appointments.models import Appointment
# Create your models here.



class AppointmentInvoice(models.Model):
    appointment = models.OneToOneField(
        'appointments.Appointment',
        on_delete=models.CASCADE,
        related_name="invoice_detail"
    )
    invoice_number = models.CharField(max_length=100, unique=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)



    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment Invoice #{self.invoice_number}"
