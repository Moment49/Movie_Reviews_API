from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import RegisterationSerializer, LoginSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import UserProfile
from rest_framework.permissions import IsAuthenticated


# Get the current User model that is active from the settings
CustomUser = get_user_model()

# Create your views here.
class ResgisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterationSerializer

@api_view(['GET', 'POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Access the validated data after the serializer validation passes
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
    
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # create the token for user
                refresh = RefreshToken.for_user(user)
                return Response({"message": "User successfully logged in", "user_data":serializer.data,'access_token':str(refresh.access_token),
                                  'refresh_token':str(refresh)}, 200)
            else:
                return Response({"message": "Username or password is incorrect"}, 400)

    else:
        return Response({"message": "Welcome to login View Form"})

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = CustomUser.objects.get(email=request.user.email)
        user_profile = UserProfile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile)       
        return Response(serializer.data)
    
    def put(self, request):
        user = CustomUser.objects.get(email=request.user)
        profile = UserProfile.objects.get(user=user)
        serializer = ProfileSerializer(profile, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({f"message":"profile updated successfully", "response_data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Error cant update profile"})

            






