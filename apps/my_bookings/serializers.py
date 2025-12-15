from rest_framework import serializers
from apps.appointments.models import Appointment 
from apps.appointments.serializers import MedicalReportSerializer
from apps.labtest.models import Test
from apps.pharmacy.models import PharmacyOrder , MedicineCoupon as PharmacyCoupon
from apps.labtest.models import Test
from apps.sponsored_packages.models import SponsoredPackage
from apps.health_packages.models import HealthPackage
from apps.pharmacy.models import PharmacyOrderItem




# class AppointmentShortSerializer(serializers.ModelSerializer):
#     voice_recording = serializers.SerializerMethodField()
#     prescription = serializers.SerializerMethodField()
#     invoice = serializers.SerializerMethodField()
#     medical_reports = MedicalReportSerializer(many=True, read_only=True)
#     voucher_available = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = [
#             "id",
#             "appointment_id",
#             "status",
#             "patient_name",
#             "mode",
#             "appointment_date",
#             "appointment_time",

#             "prescription",
#             "invoice",
#             "voice_recording",
#             "medical_reports",
#             "voucher_available",
#         ]

#     def get_voice_recording(self, obj):
#         return obj.voice_recording.url if obj.voice_recording else None

#     def get_prescription(self, obj):
#         return obj.prescription.url if obj.prescription else None

#     def get_invoice(self, obj):
#         return obj.invoice.url if obj.invoice else None

#     def get_voucher_available(self, obj):
#         return hasattr(obj, "voucher")



# class LabTestShortSerializer(serializers.ModelSerializer):
#     case_id = serializers.CharField(source="booking_id")
#     type_of_service = serializers.SerializerMethodField()

#     class Meta:
#         model = Test
#         fields = [
#             "case_id",
#             "status",
#             "patient_name",
#             "type_of_service",
#             "appointment_date",
#             "appointment_time",
#             "id"
#         ]

#     def get_type_of_service(self, obj):
#         return "Lab Test"
    

# class PharmacyOrderShortSerializer(serializers.ModelSerializer):
#     case_id = serializers.CharField(source="order_id")
#     type_of_service = serializers.SerializerMethodField()
#     order_amount = serializers.DecimalField(max_digits=10, decimal_places=2, source='total_amount')
#     expected_delivery = serializers.DateField(source='expected_delivery_date')
#     addressed_to =serializers.CharField(source='address.full_name')


#     class Meta:
#         model = Medicine
#         fields = [
#             "case_id",
#             "status",
#             "patient_name",
#             "type_of_service",
#             "ordered_date",
#             "expected_delivery",
#             "order_amount",
#             "addressed_to",
#             "id"
#         ]

#     def get_type_of_service(self, obj):
#         return "Pharmacy"

class AppointmentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id",
            "status",
            "patient_name",
            "mode",
            "appointment_date",
            "appointment_time",
        ]

class PharmacyOrderSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyOrder
        fields = [
            "order_id",
            "patient_name",
            "order_type",
            "ordered_date",
            "expected_delivery",
            "total_amount",
            "status",
        ]

class PharmacyCouponSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyCoupon
        fields = ["user_name" ,  "coupon_code","coupon_name", "vendor", "ordered_type" , "ordered_date", "status"]




class LabTestSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ["id" , "user_name","status","booked_date"]


class SponsoredPackageSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsoredPackage
        fields = ["id","user_name" ,"package_name","status"]


class HealthPackageSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthPackage
        fields = ["id" , "user_name" ,"package_name","status"]


class PharmacyOrderItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source="medicine.name", read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = PharmacyOrderItem
        fields = ['medicine_name','quantity','total_amount']

    def get_total_amount(self, obj):
        return float(obj.total_amount)