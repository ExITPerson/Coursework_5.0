from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    telegram_auth_link = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'country', 'telegram_auth_link', 'telegram_chat_id', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(password=password, **validated_data)
        print(f'is_active после создания: {user.is_active}')
        return user

    def get_telegram_auth_link(self, obj):
        return obj.get_telegram_auth_link_bot()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # можно добавить кастомные поля в токен
        return token

    def validate(self, attrs):
        # Используем email вместо username
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password'),
        }
        user = authenticate(**credentials)
        if user is None or not user.is_active:
            raise AuthenticationFailed('No active account found with the given credentials')
        return super().validate(attrs)
