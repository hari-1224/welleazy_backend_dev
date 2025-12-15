from django.shortcuts import render

# Create your views here.


from rest_framework.viewsets import ModelViewSet
from .models import (
    EyeTreatment, DentalTreatment,
    EyeVendorAddress, DentalVendorAddress,
    EyeDentalVoucher 
)
from .serializers import (
    EyeTreatmentSerializer, DentalTreatmentSerializer,
    EyeVendorSerializer, DentalVendorSerializer,
    EyeDentalVoucherCreateSerializer, EyeDentalVoucherSerializer
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from rest_framework import viewsets, permissions, status, mixins

from rest_framework.permissions import IsAuthenticated


class SmallPagination(PageNumberPagination):
    page_size = 12



class EyeTreatmentViewSet(ModelViewSet):
    queryset = EyeTreatment.objects.all()
    serializer_class = EyeTreatmentSerializer
    pagination_class = SmallPagination


class DentalTreatmentViewSet(ModelViewSet):
    queryset = DentalTreatment.objects.all()
    serializer_class = DentalTreatmentSerializer
    pagination_class = SmallPagination



class EyeVendorAddressViewSet(viewsets.ModelViewSet):
    queryset = EyeVendorAddress.objects.all()
    serializer_class = EyeVendorSerializer


class DentalVendorAddressViewSet(viewsets.ModelViewSet):
    queryset = DentalVendorAddress.objects.all()
    serializer_class = DentalVendorSerializer


class EyeDentalVoucherViewSet(ModelViewSet):
    queryset = EyeDentalVoucher.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "create":
            return EyeDentalVoucherCreateSerializer
        return EyeDentalVoucherSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return EyeDentalVoucher.objects.all()
        return EyeDentalVoucher.objects.filter(user=user)


    def retrieve(self, request, *args, **kwargs):
        voucher = self.get_object()

        if voucher.user != request.user and not request.user.is_staff:
            return Response({"detail": "You do not own this voucher"}, status=403)

        serializer = self.get_serializer(voucher)
        return Response(serializer.data)


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def activate(self, request, pk=None):
        voucher = self.get_object()
        voucher.status = 'active'
        voucher.activated_at = timezone.now()
        voucher.save()
        return Response({'status': 'activated', 'voucher_id': voucher.voucher_id_display()})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        voucher = self.get_object()
        voucher.status = 'cancelled'
        voucher.save()
        return Response({'status': 'cancelled'})
    
    
    




