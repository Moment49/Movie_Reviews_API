from rest_framework import serializers
from reviews.models import Movies, Review, ReviewComment
from rest_framework import validators
from django.contrib.auth import get_user_model



# Get the current User model that is active from the settings
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
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)

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
        movie_data= validated_data.pop('movie_title')
        movie_title = movie_data['title']
        
        try:
            movie_title = Movies.objects.get(title=movie_title)
            print(movie_title)
        except Movies.DoesNotExist:
            raise validators.ValidationError("Sorry can't review movie because we don't have such movies")    
      
        # Get the user from the request context
        user = self.context['request'].user

        if Review.objects.filter(user=user, movie_title=movie_title).exists():
            # Checks if the user has already created a review for the movie and raises appropriate error
            raise validators.ValidationError("Sorry you can not review a movie twice")

        # Creates the review if conditions pass save to the db and return the instance to be used in the view response
        movie_review = Review.objects.create(movie_title=movie_title, **validated_data)
        movie_review.save()
            

        return movie_review
    
    def update(self, instance, validated_data):
        # This method is called when the data has been validated and update is made to the db
        # Checks made here are on the data-level
        movie_data = validated_data.pop('movie_title')
        title = movie_data['title']
       
        if Movies.objects.filter(title=title).exists():
            # checks if the movie passed to the request exists before making the update
            instance.content = validated_data.get('content', instance.content)
            instance.rating = validated_data.get('rating', instance.rating)
            instance.save()
        else:
            raise validators.ValidationError("Sorry we don't have any movie matching the title")

        return instance

class CommentSerializer(serializers.ModelSerializer):
    review = ReviewSerializer()
    user = UserSerializer()
    class Meta:
        model = ReviewComment
        fields = ['id', 'review', 'user', 'content', 'created_at']


