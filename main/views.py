from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer, UserProfileSerializer, UserEditSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from main.models import UserProfile
from django.contrib.auth.models import User


class UserRegisterView(APIView):
    permission_classes = ()
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(email=serializer.initial_data['email']):
                data = {
                    'error': 'The email is already used'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user_instance = User.objects.filter(email__iexact=email)

        if user_instance:
            user_instance = User.objects.get(email__iexact=email)
            user = authenticate(username=user_instance.username, password=password)

            if user is not None:

                data = {'Token': user.auth_token.key}
                return Response(data, status=status.HTTP_200_OK)

            else:
                data = {'error': 'Wrong Credentials'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        else:
            data = {'error': 'Wrong Credentials'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ProfileLinksView(APIView):
    serializer_class = UserProfileSerializer

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):

    serializer_class = UserEditSerializer

    def put(self, request):
        serializer = UserEditSerializer(request.user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = UserEditSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

