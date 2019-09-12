from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserProfileSerializer, UserEditSerializer
from django.contrib.auth import authenticate
from main.models import UserProfile
from django.contrib.auth.models import User
from rest_framework.mixins import CreateModelMixin


class UserRegisterView(CreateModelMixin, APIView):
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(email=serializer.data['email']):
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

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            data = {'Token': user.auth_token.key}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'error': 'Wrong Credentials'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ProfileLinksView(APIView):

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

