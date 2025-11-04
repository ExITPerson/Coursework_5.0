from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    telegram_auth_link = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'country', 'telegram_auth_link', 'telegram_chat_id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(password=password, **validated_data)
        return user

    def get_telegram_auth_link(self, obj):
        return obj.get_telegram_auth_link_bot()