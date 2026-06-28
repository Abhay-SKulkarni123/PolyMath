from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from core.validators import validate_email
from .models import User, CustomerProfile, EmailVerificationToken, PasswordResetToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'date_joined', 'is_email_verified']
        read_only_fields = ['id', 'date_joined', 'is_email_verified']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=8
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(validators=[validate_email])
    first_name = serializers.CharField(required=True, min_length=2, max_length=50)
    last_name = serializers.CharField(required=True, min_length=2, max_length=50)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already registered.'})
        
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role='customer'
        )
        CustomerProfile.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=8
    )
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({'new_password': 'New passwords do not match.'})
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=8
    )
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match.'})
        
        # Verify token exists and is valid
        try:
            token_obj = PasswordResetToken.objects.get(token=data['token'])
            if not token_obj.is_valid():
                raise serializers.ValidationError({'token': 'Token is invalid or expired.'})
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({'token': 'Invalid token.'})
        
        return data

class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.UUIDField()

    def validate(self, data):
        try:
            token_obj = EmailVerificationToken.objects.get(token=data['token'])
            if not token_obj.is_valid():
                raise serializers.ValidationError({'token': 'Token is invalid or expired.'})
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError({'token': 'Invalid token.'})
        
        return data