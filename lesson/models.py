from django.db import models

from authentications.models import User


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    lesson = models.CharField(max_length=5000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'lessons'
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'


# class Vote(models.Model):
#     votes = models.IntegerField()
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#

class Like(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # like = models.BooleanField(default=False)

    class Meta:
        db_table = 'likes'
        unique_together = ['lesson', 'user']
#
# class Hate(models.Model):
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
