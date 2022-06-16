from rest_framework import serializers, permissions
from rest_framework.permissions import IsAuthenticated

from .models import User, Flight, BookingDetails, Passenger
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,)

    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    #     # For Password hash

    # def validate(self, attrs):
    #     password = attrs.get('password')
    #     password2 = attrs.get('password2')
    #     if password != password2:
    #         raise serializers.ValidationError('Password Does not match')
    #     return attrs
    #
    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     # user.set_password(validated_data['password'])
    #     # user.save()
    #     return user


class LoginSerializer(serializers.ModelSerializer):
    permission_classes = (permissions.AllowAny,)
    email = serializers.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ["email", "password"]


class ProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class UserChangePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class BookingDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingDetails
        fields = "__all__"
        depth = 1


class PassengerSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,)

    class Meta:
        model = Passenger
        fields = "__all__"
