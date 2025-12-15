from rest_framework import serializers
from .models import (HeightRecord, WeightRecord, 
                     BmiRecord, BloodPressureRecord, 
                     HeartRateRecord, OxygenSaturationRecord,
                     GlucoseRecord)

class HeightRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeightRecord
        fields = ["id", "value", "unit", "created_at", "updated_at", "created_by", "updated_by"]
        read_only_fields = ["created_at", "updated_at", "created_by", "updated_by"]
        
class WeightRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightRecord
        fields = ["id", "value", "unit", "created_at", "updated_at", "created_by", "updated_by"]
        read_only_fields = ["created_at", "updated_at", "created_by", "updated_by"] 

class BmiRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BmiRecord
        fields = ["id", "value", "unit", "created_at", "updated_at", "created_by", "updated_by"]
        read_only_fields = ["created_at", "updated_at", "created_by", "updated_by"]

class BloodPressureRecordSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField()

    class Meta:
        model = BloodPressureRecord
        fields = [
            "id", "systolic", "diastolic", "unit", "type", "category", "created_at", "updated_at", 
            "created_by", "updated_by",
        ]
        read_only_fields = ["created_at", "updated_at", "created_by", "updated_by"]
        
class HeartRateRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeartRateRecord
        fields = ["id", "value", "unit", "created_at", "updated_at", "created_by", "updated_by"]
        read_only_fields = ["created_at", "updated_at", "created_by", "updated_by"]
        
class OxygenSaturationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OxygenSaturationRecord
        fields = [ "id", "value", "unit", "created_at", "updated_at", "created_by", "updated_by"]
        read_only_fields = ["created_at", "updated_at", "created_by", "updated_by"]
        
class GlucoseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseRecord
        fields = ["id", "value", "unit", "test_type", "created_at", "updated_at", "created_by", "updated_by"]
        read_only_fields = ["created_at", "updated_at", "created_by", "updated_by"]