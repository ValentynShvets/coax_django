from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Lesson
from authentications.models import User


class LessonSerializer(serializers.ModelSerializer):
    author_email = serializers.SerializerMethodField()

    def get_author_email(self, obj):
        return obj.author.email

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'lesson', 'author', 'author_email')
        read_only_fields = ('id', 'author_email')

    def validate_user(self, value):
        self.id_ = value.get('id')
        try:
            user = User.objects.get(id=self.id_)
        except:
            raise ValidationError(f'Author not found')
    #
    # def create(self, validated_data):
    #     author = validated_data.pop('author')
    #     print(author)
    #     # user_id = User.objects.filter(email=author).values_list('pk')
    #     lesson = Lesson.objects.create(author_id=author['id'], **validated_data)
    #     return lesson
