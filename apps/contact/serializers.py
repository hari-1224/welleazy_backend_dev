from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    company_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    message = serializers.CharField()
