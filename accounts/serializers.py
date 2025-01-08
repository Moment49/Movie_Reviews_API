from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError

CustomUser = get_user_model()

class RegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
    
    def validate(self, attrs):
        """Validate the password data to ensure it meets requirements"""
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if len(password) and len(confirm_password) < 8:
            raise ValidationError('password must be greater than 8 characters')
        if password != confirm_password:
            raise ValidationError('Password does not match')
        
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        user = CustomUser.objects.create_user(email=email, username=username, password=password, first_name=first_name,
                                              last_name=last_name)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)