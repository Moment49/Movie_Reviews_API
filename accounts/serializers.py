from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError
from accounts.models import UserProfile
from reviews.models import Review

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


class ProfileSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField()
    bio = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(write_only=True)
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'profile_data']

    def get_profile_data(self, obj):
        reviews = Review.objects.filter(user=obj.user)
        review_data_list = []
        for review in reviews:
            review_data = {
                "id":review.id,
                "content": review.content,
                "rating": review.rating,
                "created_at": review.created_at
            }
            review_data_list.append(review_data)
        profile_data = {    "first_name":obj.user.first_name, 
                            "last_name": obj.user.last_name,
                            "email":obj.user.email,
                            "bio": obj.bio,
                            "profile_picture":obj.profile_picture.url,
                            "my_reviews":review_data_list
                        }
        return profile_data
    
    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)

        instance.save()
        print(instance)
        return instance