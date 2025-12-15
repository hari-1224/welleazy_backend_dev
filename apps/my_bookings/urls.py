# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import MyBookingsViewSet

# router = DefaultRouter()
# router.register(r'', MyBookingsViewSet, basename='my-bookings')
# my_bookings = MyBookingsViewSet.as_view

# urlpatterns = [
#     path('', include(router.urls)),
#     path("all/", my_bookings({'get': 'list_all'})),
#     path("scheduled/", my_bookings({'get': 'list_scheduled'})),
#     path("completed/", my_bookings({'get': 'list_completed'})),
#     path("cancelled/", my_bookings({'get': 'list_cancelled'})),
#     path("<int:pk>/upload_report/", MyBookingsViewSet.as_view({"post": "upload_report"})),
# ]


from django.urls import path
from .views import (
    MyBookingsCleanAPIView,
    # AppointmentPrescriptionDownloadView,
    PharmacyOrderMedicinesView,
    PharmacyOrderPrescriptionDownloadView,
    AppointmentVoucherView,
    PharmacyOrderVoucherView,
    PharmacyCouponVoucherView,
    LabTestVoucherView,
    SponsoredPackageVoucherView,
    HealthPackageVoucherView,
    PharmacyOrderVoucherPDFSimpleView,
    MedicalReportUploadReportView
    
)

urlpatterns = [
    path('', MyBookingsCleanAPIView.as_view(), name='my-bookings'),

    # appointment actions
    # path('appointments/<int:pk>/prescription/', AppointmentPrescriptionDownloadView.as_view(), name='appointment-prescription'),
    # path('appointments/<int:pk>/invoice/', AppointmentInvoiceDownloadView.as_view(), name='appointment-invoice'),
    path('appointments/<int:pk>/upload-report/', MedicalReportUploadReportView.as_view(), name='appointment-upload-report'),


    # pharmacy
    path('pharmacy/order/<int:pk>/medicines/', PharmacyOrderMedicinesView.as_view(), name='pharmacy-order-medicines'),
    path('pharmacy/order/<int:pk>/prescription/', PharmacyOrderPrescriptionDownloadView.as_view(), name='pharmacy-order-prescription'),
    # path('pharmacy/order/<int:pk>/invoice/', PharmacyOrderInvoiceDownloadView.as_view(), name='pharmacy-order-invoice'),

   # For Vouchers to view
    # Appointments
    path("appointments/<int:pk>/voucher/", AppointmentVoucherView.as_view()),
    # Pharmacy order
    path("pharmacy/order/<int:pk>/voucher/", PharmacyOrderVoucherView.as_view()),
    # Pharmacy coupon
    path("pharmacy-coupon/<int:pk>/voucher/", PharmacyCouponVoucherView.as_view()),
    # Lab test
    path("labtest/<int:pk>/voucher/", LabTestVoucherView.as_view()),
    # Sponsored package
    path("sponsored-package/<int:pk>/voucher/", SponsoredPackageVoucherView.as_view()),
    # Health package
    path("health-package/<int:pk>/voucher/", HealthPackageVoucherView.as_view()),

    path("pharmacy/order/<int:pk>/voucher/download/pdf/", 
         PharmacyOrderVoucherPDFSimpleView.as_view(),
         name="pharmacy-order-voucher-pdf"),

]



