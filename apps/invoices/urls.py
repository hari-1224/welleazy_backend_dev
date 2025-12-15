from django.urls import path
from .views import AppointmentInvoiceDetailAPIView, AppointmentInvoicePDFAPIView

urlpatterns = [
    path("appointment/<int:appointment_id>/invoice/", 
         AppointmentInvoiceDetailAPIView.as_view()),

    path("appointment/<int:appointment_id>/invoice/pdf/",
         AppointmentInvoicePDFAPIView.as_view()),
]
