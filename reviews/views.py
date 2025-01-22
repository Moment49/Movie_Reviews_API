from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView, DestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from reviews.serializers import ReviewSerializer, MovieSerializer, UserSerializer, CommentSerializer
from rest_framework import status
from reviews.models import Review, LikeReviews, ReviewComment
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from reviews.permissions import CustomPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.validators import ValidationError
from reviews.pagination import CustomPagination
from reviews.filters import ReviewFilter
from rest_framework.decorators import action
from django.db.models import Count

# Get the current User model that is active from the settings
CustomUser = get_user_model()

# Create your views here.
class MovieReviewView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['movie_title__title', 'rating']
    ordering_fields = ['created_at']
    filterset_class = ReviewFilter

    @action(detail=True, methods=['get'])
    def like(self, request, pk=None):
        print(self.get_object())
        likes_by_user = LikeReviews.objects.filter(user=request.user, review=self.get_object())
        if likes_by_user.exists():
            return Response({"message":"You have already liked this review"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            liked_review = LikeReviews.objects.create(user=request.user, review=self.get_object())
            liked_review.save()
        return Response({"message":"review liked"})
    
    @action(detail=True, methods=['get'])
    def unlike(self, request, pk=None):
        print(self.get_object())
        likes_by_user = LikeReviews.objects.get(user=request.user, review=self.get_object())
        if likes_by_user:
            likes_by_user.delete()
        
        return Response({"message": "review unliked"})

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class MostLikedReviewByMovie(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, movie_id=None):
        # We use the anotate to get the agregate count for the number of likes for reviews based on a particular movie(likes are sorted)
        reviews = Review.objects.annotate(num_like=Count("likes")).filter(movie_title=movie_id).order_by('-num_like')
        review_list = []
        for review in reviews:
            # Serialize the review data and retrieve the necessary details to be displayed
            serializer = ReviewSerializer(review)
            most_review_likes_data = {
                "review_id": serializer.data['id'],
                "movie_title":serializer.data['movie_title']['title'],
                "content":serializer.data['content'],
                "rating": serializer.data['rating'],
                "user": serializer.data['user']['email'],
                "created_at": serializer.data['created_at'], 
                "likes_count":review.num_like
            }
            review_list.append(most_review_likes_data)
        return Response({"review_data":f"{review_list}"})


class MovieReviewByTitle(APIView, CustomPagination):
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        # Get request to return title from the query params
        title = request.GET.get('title')

        review_by_movie = Review.objects.filter(movie_title__title__icontains=title).order_by('-created_at')

        # List to hold the moview_review iterable
        movie_review_list = []
        # Paginate the query set 
        self.paginate_queryset(review_by_movie, request, view=self)

        for mv_t in review_by_movie:
            # Iterate through the the query set
            movie_title = MovieSerializer(mv_t.movie_title)
            user = UserSerializer(mv_t.user)

            # serialize the return data to a json format to return the paginated response    
            movie_data = {
                "id": mv_t.id,
                "movie_tite":movie_title.data['title'],
                "content": mv_t.content,
                "rating":mv_t.rating,
                "created_at":mv_t.created_at,
                "user":user.data['email'],
            }  
            movie_review_list.append(movie_data)  
        
        return self.get_paginated_response(movie_review_list)
        

class UserDetailView(APIView):
    """This is the User Detail view to display all the user data"""
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        user = generics.get_object_or_404(CustomUser, pk=user_id)
        serializer = UserSerializer(user)
        return Response({"user_details":serializer.data}, 200)
    

class UserDeleteView(GenericAPIView):
    """This is the delete view for the user """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id=None):
        user_obtained_id = CustomUser.objects.get(pk=user_id)
        user_req = self.request.user
        if user_req == user_obtained_id:
            # Condidition to check if the request.user matches the user_id passed
            # view-level permission check for the object.
            user_req.delete()
            return Response({"message":"user deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"You can't delete another user"}, status=status.HTTP_403_FORBIDDEN)

class UserUpdateView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    

    def patch(self, request, pk=None):
        return self.update_user(request, pk, partial=True)
        
    def put(self, request, pk=None):
        return self.update_user(request, pk, partial=False)

    def update_user(self, request, pk, partial):
        # Method to partially update user records
        user = CustomUser.objects.get(email=request.user)
        user_pk = CustomUser.objects.get(pk=pk)
        if user == user_pk:
            serializer = UserSerializer(user, data=request.data, partial=partial)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': f'user updated successfully', "user_details":serializer.data},status=status.HTTP_200_OK)
        else:
            print("Bad request")
            return Response({'message': "Bad Request"},status=status.HTTP_400_BAD_REQUEST)
        

class ReviewCommentCreateView(ListCreateAPIView):
    queryset = ReviewComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CustomPermission]

    def get(self, request, review_id=None, *args, **kwargs):
        review = Review.objects.get(pk=review_id)
        reviews = ReviewComment.objects.filter(review=review)
        if reviews:
            serializer = CommentSerializer(reviews, many=True)
            return Response({"data": serializer.data})
        return Response({"message": "No comments for review"}, status=status.HTTP_204_NO_CONTENT)
            
    def post(self, request, review_id=None, *args, **kwargs):
        review_data_id = request.data['review']
        if review_id != review_data_id:
            return Response({"error":"Review with id passed does not match"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                Review.objects.get(pk=review_id)
            except Review.DoesNotExist:
                raise ValidationError("Review with id does not exist")
        serializer = self.get_serializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)    

class ReviewCommentUpdateView(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    queryset = ReviewComment.objects.all()

    def put(self, request, pk=None, review_id=None):
        # Get the comment obj which will trigger the obj-level permission check 
        review_comment = self.get_object()
        # Get the review from the request body and check if it matches with the path params passed
        review_data_id = request.data['review']
        if review_id != review_data_id:
            return Response({"error":"Sorry!! this review does not match with id specified"}, status=status.HTTP_400_BAD_REQUEST)
        # Extra validation check to if the review is associated with the comment to be updated
        review = Review.objects.get(pk=review_id)
        if review.id != review_comment.review.id:
            return Response({"error":"Sorry this comment is not associated with the specified review"}, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = CommentSerializer(review_comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"updated successfully", 'data':serializer.data}, status=status.HTTP_200_OK)
        
class ReviewCommentDeleteView(DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    queryset = ReviewComment.objects.all()

    def destroy(self, request, pk=None, review_id=None, *args, **kwargs):
        instance = self.get_object()
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return Response({"error":f"Review with id {review_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_destroy(instance)
        return Response({"message":f"comment `{instance.content}`successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
            
            




    

