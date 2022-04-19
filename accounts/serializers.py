from django.db.utils import IntegrityError
from rest_framework import serializers

from accounts.models import User


class AccountSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, required=True)
    password = serializers.CharField(min_length=6, required=True)


class SignUpSerializer(AccountSerializer):

    def create(self, validated_data):
        try:
            user = User.objects.create(username=validated_data.get('username'))
        except IntegrityError:
            raise serializers.ValidationError({"username": "Username already taken."})

        user.set_password(raw_password=validated_data.get('password'))
        user.save()

        return user
