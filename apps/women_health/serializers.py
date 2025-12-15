
from rest_framework import serializers
from .models import WomanProfile, Symptoms, CycleEntry

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptoms
        fields = ["id", "name"]

class WomanProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WomanProfile
        fields = ["id", "age", "created_at"]

class CycleEntrySerializer(serializers.ModelSerializer):
    # allow passing symptom IDs
    symptoms = serializers.PrimaryKeyRelatedField(
        queryset=Symptoms.objects.all(),
        many=True,
        write_only=True
    )

    symptom_details = serializers.SerializerMethodField()
    # computed read-only fields
    next_period_start = serializers.DateField(read_only=True)
    next_period_end = serializers.DateField(read_only=True)
    ovulation_date = serializers.DateField(read_only=True)
    fertile_window_start = serializers.DateField(read_only=True)
    fertile_window_end = serializers.DateField(read_only=True)

    class Meta:
        model = CycleEntry
        fields = [
            "id",
            "profile",
            "avg_period_length",
            "avg_cycle_length",
            "last_period_start",
            "symptoms",
            "symptom_details",
            "next_period_start",
            "next_period_end",
            "ovulation_date",
            "fertile_window_start",
            "fertile_window_end",
            "created_at",
        ]
        read_only_fields = ["symptom_details","next_period_start", "next_period_end", "ovulation_date", "fertile_window_start", "fertile_window_end", "created_at"]



    def get_symptom_details(self, obj):
        return [sym.name for sym in obj.symptoms.all()]
    

    def create(self, validated_data):
        symptoms = validated_data.pop("symptoms", [])
        entry = CycleEntry.objects.create(**validated_data)
        if symptoms:
            entry.symptoms.set(symptoms)
        return entry

    

    

   

    
