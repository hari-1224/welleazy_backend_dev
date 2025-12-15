from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import GymCenter, GymPackage, Voucher, Dependant
from .serializers import (
    GymCenterSerializer, GymPackageSerializer,
    VoucherCreateSerializer, VoucherDetailSerializer,
    DependantSerializer
)

class GymCenterViewSet(viewsets.ModelViewSet):
    queryset = GymCenter.objects.all().order_by('name')
    serializer_class = GymCenterSerializer
    permission_classes = [permissions.AllowAny]


class GymPackageViewSet(viewsets.ModelViewSet):
    queryset = GymPackage.objects.all().order_by('duration_months')
    serializer_class = GymPackageSerializer
    permission_classes = [permissions.AllowAny]


class VoucherViewSet(viewsets.ModelViewSet):
   
    queryset = Voucher.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create']:
            return VoucherCreateSerializer
        return VoucherDetailSerializer

    def get_queryset(self):
        # users can see only their vouchers unless staff
        user = self.request.user
        if user.is_staff:
            return Voucher.objects.all().order_by('-created_at')
        return Voucher.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def activate(self, request, pk=None):
        # Admin or vendor can later set activation code, mark voucher active
        voucher = self.get_object()
        voucher.status = 'active'
        voucher.activated_at = timezone.now()
        voucher.save()
        return Response({'status': 'activated', 'voucher_id': voucher.voucher_id_display()})
    

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        voucher = self.get_object()
        voucher.status = "cancelled"
        voucher.save()
        return Response({"status": "cancelled" , "voucher_id": voucher.voucher_id_display()})
    

    @action(detail=True, methods=['post'])
    def fail(self, request, pk=None):
        voucher = self.get_object()
        voucher.status = "failed"
        voucher.save()
        return Response({"status": "failed"})


