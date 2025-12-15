import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.appointments.models import Appointment
from .models import AppointmentInvoice


@receiver(post_save, sender=Appointment)
def generate_appointment_invoice(sender, instance, created, **kwargs):

    # Generate invoice only when appointment is PAID or COMPLETED
    if instance.status not in ["paid", "completed"]:
        return  

    # Prevent duplicate invoices
    if hasattr(instance, "invoice"):
        return

    consultation_fee = instance.fee_amount
    gst_amount = float(consultation_fee) * 0.18
    total = float(consultation_fee) + gst_amount

    AppointmentInvoice.objects.create(
        appointment=instance,
        invoice_number=str(uuid.uuid4()).split("-")[0].upper(),
        consultation_fee=consultation_fee,
        gst_amount=gst_amount,
        total_amount=total,
        payment_mode=instance.payment_mode,
        payment_bank=instance.payment_bank,
        payment_reference=instance.payment_reference,
        payment_transaction_id=instance.payment_transaction_id,
        payment_last4=instance.payment_last4,
    )
