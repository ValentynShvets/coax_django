from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentications.serializers import UserSerializer
# from .views import *
from .models import Lesson
from authentications.models import User


class LessonSerializer(serializers.ModelSerializer):
    # User = UserSerializer()
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'lesson', 'author')
        read_only_fields = ('id',)

    def validate_user(self, value):
        self.id_ = value.get('id')
        try:
            user = User.objects.get(id=self.id_)
        except:
            raise ValidationError(f'Author not found')

    def create(self, validated_data):
        author = validated_data.pop('author')
        user_id = User.objects.filter(email=author).values_list('pk')
        lesson = Lesson.objects.create(author_id=user_id[0][0], **validated_data)
        return lesson
