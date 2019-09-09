from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from main.models import UserProfile


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class UserEditSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ('user',)
