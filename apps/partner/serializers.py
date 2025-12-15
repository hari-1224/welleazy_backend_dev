from rest_framework import serializers

class PartnerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    business_type = serializers.CharField(max_length=200)
    phone_number = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    message = serializers.CharField()
