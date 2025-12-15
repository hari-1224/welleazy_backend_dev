from rest_framework import serializers
from apps.dependants.serializers import DependantSerializer

class DependantResolverMixin(serializers.Serializer):

    dependant = serializers.SerializerMethodField()
    dependant_data = serializers.SerializerMethodField()

    def get_dependant(self, obj):

        if obj.for_whom == "self":
            return None
        return obj.dependant.id if obj.dependant else None

    def get_dependant_data(self, obj):
        request = self.context.get("request")

        # For Self
        if obj.for_whom == "self":
            user = request.user if request else None
            if not user:
                return None

            name = (
                getattr(user, "first_name", None)
                or getattr(user, "full_name", None)
                or getattr(user, "name", None)
                or user.email
                or user.username
            )

            return {
                "id": user.id,
                "name": name,
                "relationship": "Self"
            }

        # For dependant
        if obj.dependant:
            return DependantSerializer(obj.dependant).data

        return None
