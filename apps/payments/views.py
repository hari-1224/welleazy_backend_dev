# apps/payments/views.py

import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.appointments.models import Cart
from apps.appointments.models import Appointment as AppointmentModel, AppointmentItem

from django.views.generic import TemplateView

class CreateRazorpayOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, cart_id):

        cart = get_object_or_404(Cart, id=cart_id, user=request.user)
        items = cart.items.all()

        if not items.exists():
            return Response({"detail": "Cart is empty"}, status=400)

        # Final payable amount after discounts
        final_amount = sum(float(item.final_price or 0) for item in items)
        amount_paise = int(final_amount * 100)   # Razorpay expects paise

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        # Create Order
        order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1,
            "notes": {
                "cart_id": str(cart.id),
                "user_id": str(request.user.id)
            }
        })

        return Response({
            "message": "Order created successfully",
            "order_id": order["id"],
            "amount": final_amount,
            "currency": "INR",
            "key_id": settings.RAZORPAY_KEY_ID
        })

class RazorpayVerifyPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get("razorpay_payment_id")
        order_id = request.data.get("razorpay_order_id")
        signature = request.data.get("razorpay_signature")

        if not all([payment_id, order_id, signature]):
            return Response({"detail": "Missing fields"}, status=400)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        # Verify Razorpay signature
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })
        except:
            return Response({"detail": "Invalid payment signature"}, status=400)

        # Fetch the order to get cart_id
        order_info = client.order.fetch(order_id)
        cart_id = order_info["notes"].get("cart_id")

        cart = get_object_or_404(Cart, id=cart_id)
        items = cart.items.all()

        if not items.exists():
            return Response({"detail": "Cart is empty"}, status=400)

        created = []

        # Create appointments
        for item in items:
            appt = AppointmentModel.objects.create(
                user=request.user,
                diagnostic_center=item.diagnostic_center,
                visit_type=item.visit_type,
                for_whom=item.for_whom,
                dependant=item.dependant,
                address=item.address,
                note=item.note,
                status="confirmed",
                created_by=request.user,
                updated_by=request.user
            )

            for t in item.tests.all():
                AppointmentItem.objects.create(
                    appointment=appt,
                    test=t,
                    price=t.price
                )

            created.append({
                "appointment_id": appt.id,
                "diagnostic_center": appt.diagnostic_center.name,
                "tests": [t.name for t in item.tests.all()]
            })

        # Empty cart after payment
        cart.items.all().delete()

        return Response({
            "message": "Payment verified, appointments confirmed",
            "appointments": created
        })


class RazorpayPaymentPageView(TemplateView):
    template_name = "payments/payment_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_id"] = kwargs.get("cart_id")
        
        context["access_token"] = self.request.GET.get("token", "")
        return context
