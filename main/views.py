from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import authenticate


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()


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

