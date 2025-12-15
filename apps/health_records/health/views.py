from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from apps.common.mixins.save_user_mixin import SaveUserMixin
from apps.accounts.models import UserProfile 
from .models import (HeightRecord, WeightRecord, 
                     BmiRecord, BloodPressureRecord, 
                     HeartRateRecord, OxygenSaturationRecord,
                     GlucoseRecord)
from .serializers import (HeightRecordSerializer, WeightRecordSerializer, 
                          BmiRecordSerializer, BloodPressureRecordSerializer, 
                          HeartRateRecordSerializer, OxygenSaturationRecordSerializer,
                          GlucoseRecordSerializer)


class HeightRecordViewSet(SaveUserMixin, viewsets.ModelViewSet):
    serializer_class = HeightRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HeightRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def latest(self, request):
        record = self.get_queryset().order_by("-updated_at").first()
        if record:
            serializer = self.get_serializer(record)
            return Response(serializer.data)
        return Response({"detail": "No height record found."}, status=404)

class WeightRecordViewSet(SaveUserMixin, viewsets.ModelViewSet):
    serializer_class = WeightRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WeightRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def latest(self, request):
        record = self.get_queryset().order_by("-updated_at").first()
        if record:
            serializer = self.get_serializer(record)
            return Response(serializer.data)
        return Response({"detail": "No weight record found."}, status=404)
    
class BmiRecordViewSet(SaveUserMixin, viewsets.ModelViewSet):
    serializer_class = BmiRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BmiRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def latest(self, request):
        record = self.get_queryset().order_by("-updated_at").first()
        if record:
            serializer = self.get_serializer(record)
            return Response(serializer.data)
        return Response({"detail": "No BMI record found."}, status=404)
    
class BloodPressureRecordViewSet(SaveUserMixin, viewsets.ModelViewSet):
    serializer_class = BloodPressureRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BloodPressureRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def latest(self, request):
        record = self.get_queryset().order_by("-updated_at").first()
        if record:
            serializer = self.get_serializer(record)
            return Response(serializer.data)
        return Response({"detail": "No blood pressure record found."}, status=404)
    
class HeartRateRecordViewSet(SaveUserMixin, viewsets.ModelViewSet):
    serializer_class = HeartRateRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HeartRateRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def latest(self, request):
        record = self.get_queryset().order_by("-updated_at").first()
        if record:
            serializer = self.get_serializer(record)
            return Response(serializer.data)
        return Response({"detail": "No heart rate record found."}, status=404)
    
class OxygenSaturationRecordViewSet(SaveUserMixin, viewsets.ModelViewSet):
    serializer_class = OxygenSaturationRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OxygenSaturationRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def latest(self, request):
        record = self.get_queryset().order_by("-updated_at").first()
        if record:
            serializer = self.get_serializer(record)
            return Response(serializer.data)
        return Response({"detail": "No O₂ saturation record found."}, status=404)
    
class GlucoseRecordViewSet(SaveUserMixin, viewsets.ModelViewSet):
    serializer_class = GlucoseRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GlucoseRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def latest(self, request):
        record = self.get_queryset().order_by("-updated_at").first()
        if record:
            serializer = self.get_serializer(record)
            return Response(serializer.data)
        return Response({"detail": "No glucose record found."}, status=404)
    
@api_view(["GET"])
def blood_group(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        blood_group = profile.blood_group
    except UserProfile.DoesNotExist:
        blood_group = None

    return Response({"blood_group": blood_group})
    
@api_view(["GET"])
def health_record_choices(request):
    data = {
        "height_units": dict(HeightRecord.UNIT_CHOICES),
        "weight_units": dict(WeightRecord.UNIT_CHOICES),
        "blood_pressure_units": dict(BloodPressureRecord.UNIT_CHOICES),
        "blood_pressure_types": dict(BloodPressureRecord.TYPE_CHOICES),
        "bmi_units": dict(BmiRecord.UNIT_CHOICES),
        "heart_rate_units": dict(HeartRateRecord.UNIT_CHOICES),
        "oxygen_saturation_units": dict(OxygenSaturationRecord.UNIT_CHOICES),
        "glucose_units": dict(GlucoseRecord.UNIT_CHOICES),
        "glucose_test_types": dict(GlucoseRecord.TYPE_CHOICES),
    }
    return Response(data)