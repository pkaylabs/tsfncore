from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import User
from apis.models import Notification, School, Report


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']


class LoginSerializer(serializers.Serializer):
    '''Serializer for user login'''
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and ((hasattr(user, "deleted") and user.deleted == False) or not hasattr(user, "deleted")):
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    class Meta:
        model = User
        fields = ('email', 'phone', 'password', 'name', 'address', 'region', 'district')
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure the password is not included in responses
            'email': {'required': True},       # Email is required during registration
            'phone': {'required': True},       # Phone is required during registration
        }

    def validate(self, attrs):
        """Validate the data to ensure the email and phone are unique."""
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError("Email already exists")
        if User.objects.filter(phone=attrs.get('phone')).exists():
            raise serializers.ValidationError("Phone already exists")
        return attrs

    def create(self, validated_data):
        """Create a new user instance."""
        user = User.objects.create_user(
            phone=validated_data.get('phone'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            name=validated_data.get('name'),
            address=validated_data.get('address'),
            region=validated_data.get('region'),
            district=validated_data.get('district'),
        )
        return user
    

class SchoolSerializer(serializers.ModelSerializer):
    '''Serializer for the School model'''
    class Meta:
        model = School
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    '''Serializer for the Notification model'''
    reporter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Notification
        fields = '__all__'


class GetReportSerializer(serializers.ModelSerializer):
    '''Serializer for the Report model'''
    school = SchoolSerializer()
    reported_by = UserSerializer()
    get_report_images = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Report
        fields = '__all__'

class AddReportSerializer(serializers.ModelSerializer):
    '''Serializer for the Report model'''
    class Meta:
        model = Report
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    '''Serializer for changing password'''
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        return data
    

class ResetPasswordSerializer(serializers.Serializer):
    '''Serializer for resetting password'''
    phone = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(phone=data.get('phone')).exists():
            raise serializers.ValidationError("Phone does not exist")
        return data