from rest_framework import serializers

class NotFoundSerializers(serializers.Serializer):
    detail = serializers.CharField(default='Not Found')


