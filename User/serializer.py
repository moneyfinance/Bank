from rest_framework import serializers
from .models import Otp,User
from django.core.validators import RegexValidator

class Otp_serializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError('Invalid phone number format. Must be 10 digits.')
        return value
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number','is_phone_verified','first_name','last_name']

    def create(self,validated_data):
        return User.objects.create_user(**validated_data) 
