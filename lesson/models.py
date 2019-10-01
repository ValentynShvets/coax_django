from django.db import models

from authentications.models import User


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    lesson = models.CharField(max_length=5000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# class Vote(models.Model):
#     votes = models.IntegerField()
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#
#
# class Like(models.Model):
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#
# class Hate(models.Model):
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
