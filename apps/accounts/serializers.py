from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, PasswordResetToken, UserOTP, UserProfile
import hashlib, re

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password", "name", "mobile_number"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def validate_mobile_number(self, value):
        if User.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number already registered")
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")  # remove confirm_password before saving
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs.get("email"), password=attrs.get("password"))
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs["user"] = user
        return attrs


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not found")
        return value


class ResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            token_obj = PasswordResetToken.objects.get(token=attrs["token"])
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token")

        if not token_obj.is_valid():
            raise serializers.ValidationError("Token expired or already used")

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})

        attrs["token_obj"] = token_obj
        return attrs

    def save(self, **kwargs):
        token_obj = self.validated_data["token_obj"]
        user = token_obj.user
        user.set_password(self.validated_data["new_password"])
        user.save()
        token_obj.mark_used() # Mark the token as used
        return user

class RequestOTPSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # can be email or mobile

    def validate_identifier(self, value):
        value = value.strip()

        # Check if it's an email
        if re.match(r"[^@]+@[^@]+\.[^@]+", value):
            method = "email"
            user = User.objects.filter(email=value).first()
            formatted_value = value  # email stays as is
        else:
            # Validate mobile number (only 10 digits allowed)
            if not re.match(r"^[6-9]\d{9}$", value):
                raise serializers.ValidationError("Enter a valid 10-digit Indian mobile number")

            method = "mobile"
            user = User.objects.filter(mobile_number=value).first()

            # Format number for Twilio
            formatted_value = f"+91{value}"

        if not user:
            raise serializers.ValidationError("User not found")

        # Store values for use in the view
        self.context["method"] = method
        self.context["user"] = user
        self.context["formatted_value"] = formatted_value  # formatted for Twilio

        return value
  
class VerifyOTPSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, attrs):
        identifier = attrs["identifier"]
        otp_plain = attrs["otp"]

        if re.match(r"[^@]+@[^@]+\.[^@]+", identifier):
            method = "email"
            user = User.objects.filter(email=identifier).first()
        else:
            method = "mobile"
            user = User.objects.filter(mobile_number=identifier).first()

        if not user:
            raise serializers.ValidationError("User not found")

        otp_hash = hashlib.sha256(otp_plain.encode()).hexdigest()

        try:
            otp_obj = UserOTP.objects.filter(user=user, otp_hash=otp_hash, method=method).latest("created_at")
        except UserOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP")

        if not otp_obj.is_valid():
            raise serializers.ValidationError("OTP expired or already used")

        attrs["user"] = user
        attrs["otp_obj"] = otp_obj
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Custom JWT serializer to include message and user data
    def validate(self, attrs):
        data = super().validate(attrs)

        new_data = {
            "message": "Login successful",
            "refresh": data["refresh"],
            "access": data["access"],
            "user": {
                "id": self.user.id,
                "email": self.user.email,
                "name": self.user.name,
            }
        }

        return new_data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "personal_email",
            "gender",
            "dob",
            "marital_status",
            "blood_group",
            "corporate_name",
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "mobile_number",
            "member_id",
            "employee_id",
            "profile",
        ]
        read_only_fields = ["email", "member_id", "employee_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make mobile number optional (not required on update)
        self.fields["mobile_number"].required = False

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})

        # Update editable user fields
        for attr, value in validated_data.items():
            # Skip any read-only fields
            if attr not in self.Meta.read_only_fields:
                setattr(instance, attr, value)
        instance.save()

        # Update profile
        profile, _ = UserProfile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance