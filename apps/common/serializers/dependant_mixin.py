from rest_framework import serializers
from apps.dependants.serializers import DependantSerializer

class DependantResolverMixin(serializers.Serializer):

    dependant = serializers.SerializerMethodField()
    dependant_data = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()

    def get_dependant(self, obj):

        if obj.for_whom == "self":
            return None
        return obj.dependant.id if obj.dependant else None

    def get_dependant_data(self, obj):
        request = self.context.get("request")

        if obj.for_whom == "self":
            return None

        # For dependant
        if obj.dependant:
            return DependantSerializer(obj.dependant).data

        return None

    def get_patient_name(self, obj):
        request = self.context.get("request")
        
        # 1. Self logic
        if obj.for_whom == "self":
            user = request.user if request else getattr(obj, "user", None) 
            # Fallback if obj has .user (some models might)
            
            if user:
                 return (
                    getattr(user, "first_name", None)
                    or getattr(user, "full_name", None) # if custom user model
                    or getattr(user, "name", None)
                    or user.email
                )
            return "Self"

        # 2. Dependant logic
        if obj.dependant:
            return obj.dependant.name
            
        return "Unknown"
