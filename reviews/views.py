from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from reviews.serializers import ReviewSerializer, MovieSerializer, UserSerializer
from rest_framework import status
from reviews.models import Review, Movies
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from reviews.permissions import CustomPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.validators import ValidationError

CustomUser = get_user_model()

# Create your views here.
class MovieReviewView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated, CustomPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['movie_title__title']
    search_fields = ['movie_title__title', 'rating']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class MovieReviewByTitle(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        title = request.GET.get('title')
        print(title)
        review_by_movie = Review.objects.filter(movie_title__title=title)
        movie_review_list = []
        for mv_t in review_by_movie:
            movie_title = MovieSerializer(mv_t.movie_title)
            user = UserSerializer(mv_t.user)
           
            movie_data = {
                "id": mv_t.id,
                "movie_tite":movie_title.data,
                "content": mv_t.content,
                "rating":mv_t.rating,
                "user":user.data,
            }  
            movie_review_list.append(movie_data)  
        print(movie_review_list)   
        return Response({"data":movie_review_list})
        

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        user = generics.get_object_or_404(CustomUser, pk=user_id)
        serializer = UserSerializer(user)
        return Response({"user_details":serializer.data}, 200)
    

class UserDeleteView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id=None):
        user_obtained_id = CustomUser.objects.get(pk=user_id)
        user_req = self.request.user
        if user_req == user_obtained_id:
            user_req.delete()
            return Response({"message":"user deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"You can't delete another user"}, status=status.HTTP_403_FORBIDDEN)

class UserUpdateView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
 
    def patch(self, request, pk=None):
        # Method to partial update user records
        user = CustomUser.objects.get(email=request.user)
        user_pk = CustomUser.objects.get(pk=pk)
        if user == user_pk:
            serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': f'user updated successfully', "user_details":serializer.data},status=status.HTTP_200_OK)
        else:
            print("Bad request")
            return Response({'message': "Bad Request"},status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None):
        # Method to partial update user records
        user = CustomUser.objects.get(email=request.user)
        user_pk = CustomUser.objects.get(pk=pk)
        if user == user_pk:
            serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': f'user updated successfully', "user_details":serializer.data},status=status.HTTP_200_OK)
        else:
            print("Bad request")
            return Response({'message': "Bad Request"},status=status.HTTP_400_BAD_REQUEST)

    

