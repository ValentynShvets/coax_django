from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
import json
from Coax.tests import BaseAPITest
from lesson.models import Lesson


class TestLessonView(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        # print(self.user)
        self.lesson_dict = {
            "title": "stringee",
            "lesson": "string",
            "author": self.user.id
        }
        # raise ValueError(self.user)
        self.lesson = mixer.blend(Lesson, title="title", lesson='lesson', author=self.user)

    def test_lessons_list(self):
        resp = self.client.get(reverse('lesson:lessons-list'))
        self.assertEqual(resp.status_code, 200)

    def test_lessons_retrieve(self):
        resp = self.client.get(reverse('lesson:lessons-detail', args=(self.lesson.id,)))
        self.assertEqual(resp.status_code, 200)

    def test_lessons_create(self):
        count = Lesson.objects.all().count()
        resp = self.client.post(reverse('lesson:lessons-list'), data=json.dumps(self.lesson_dict),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(count + 1, Lesson.objects.all().count())

    def test_lessons_update(self):
        self.lesson_dict['title'] = 'sdfkhshkfdshkfsdhfjsdhkfshdkfj'
        resp = self.client.put(reverse('lesson:lessons-detail', args=(self.lesson.id,)),
                               data=json.dumps(self.lesson_dict), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        # self.assertEqual(count + 1, Lesson.objects.all().count())
    def test_lessons_retrieve_invalid(self):
        resp = self.client.get(reverse('lesson:lessons-detail', args=(11111,)))
        self.assertEqual(resp.status_code, 404)

    def test_lessons_create_invalid(self):
        self.lesson_dict['author'] = 11111
        # count = Lesson.objects.all().count()
        resp = self.client.post(reverse('lesson:lessons-list'), data=json.dumps(self.lesson_dict),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        # self.assertEqual(count + 1, Lesson.objects.all().count())

    def test_lessons_update_invalid(self):
        self.lesson_dict['title'] = 'sdfkhshkfdshkfsdhfjsdhkfshdkfj'
        resp = self.client.put(reverse('lesson:lessons-detail', args=(12121212,)),
                               data=json.dumps(self.lesson_dict), content_type='application/json')
        self.assertEqual(resp.status_code, 404)

    def test_lessons_delete(self):
        resp = self.client.delete(reverse('lesson:lessons-detail', args=(self.lesson.id,)))
        self.assertEqual(resp.status_code, 204)

    def test_lessons_delete_invalid(self):
        resp = self.client.delete(reverse('lesson:lessons-detail', args=(11111,)))
        self.assertEqual(resp.status_code, 404)
