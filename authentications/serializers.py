from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()
        return user

    class Meta(object):
        model = User
        fields = ('id', 'email', 'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}
