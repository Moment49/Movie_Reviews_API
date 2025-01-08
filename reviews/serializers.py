from rest_framework import serializers
from reviews.models import Movies, Review
from rest_framework import validators
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['title']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields = ['email', 'first_name', 'last_name', 'username']
    
    def update(self, instance, validated_data):
        # This method handles update of validated_data passed to the serializer
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        username = validated_data.pop('username')
        instance.email = email
        instance.first_name = first_name
        instance.last_name = last_name
        instance.username = username
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    # This holds the nested serializer for the data relationships for both user and movie_title
    user = UserSerializer(read_only=True)
    movie_title = MovieSerializer()
    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'content', 'rating', 'user', 'created_at']
           
    def create(self, validated_data):
        try:
            movie_data= validated_data.pop('movie_title')
            movie_title = movie_data['title']
            movie_title = Movies.objects.get(title = movie_title)
        except Movies.DoesNotExist:
            movie_title = Movies.objects.create(title=movie_title)
            movie_title.save()
    
        movie_review = Review.objects.create(movie_title=movie_title, **validated_data)
        movie_review.save()

        return movie_review
    
    def update(self, instance, validated_data):
        content = validated_data.pop('content')
        rating = validated_data.pop('rating')
        instance.content = content
        instance.rating = rating

        instance.save()

        return instance