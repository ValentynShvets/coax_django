from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import status, viewsets
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import *

from django.contrib import messages
from .models import *


class MainView(TemplateView):
    context = {}
    template_name = "lesson/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(data=Lesson.objects.all(), **kwargs)
        all_lesson = Lesson.objects.all().order_by('-id')
        page = self.request.GET.get('page')
        all_pages = Paginator(all_lesson, 5)
        if page is None:
            page = 1
        elif int(page) > all_pages.num_pages:
            page = all_pages.num_pages
        pages = all_pages.get_page(page)
        context['page_num'] = all_lesson
        context['page_num'] = int(page)
        context['end_page'] = all_pages.num_pages
        context['pages'] = pages
        # context['likes'] = {}
        # for page in pages:
        #     print(page)
        # likes = Like.objects.all()
        # # print(likes)
        # for like in likes:
        #     count = Like.objects.filter(lesson_id=like.lesson_id, like=True).count()
        #     context['likes'][f'{like.lesson_id}'] = count

        return context


class EditLesson(TemplateView):
    context = {}
    template_name = "lesson/edit_lesson.html"

    def get_context_data(self, *args, **kwargs):
        lesson_id = self.request.GET.get('lesson_id')
        context = super().get_context_data(lesson=Lesson.objects.get(pk=lesson_id))
        # less = Lesson.objects.get(pk=lesson_id)
        return context

    def get(self, *args, **kwargs):
        lesson_id = self.request.GET.get('lesson_id')
        context = super().get(Lesson.objects.get(pk=lesson_id))
        context['lesson'] = Lesson.objects.get(pk=lesson_id)
        less = Lesson.objects.get(pk=lesson_id)
        if not self.request.user.is_superuser and less.author.id != self.request.user.id:
            messages.success(self.request, f"You aren`t the author of this lesson ")
            return HttpResponseRedirect(reverse('home'))

        return context

    def post(self, *args, **kwargs):
        lesson_id = self.request.GET.get('lesson_id')
        if self.request.POST.get('title') and self.request.POST.get('lesson'):
            reload = Lesson.objects.get(pk=lesson_id)
            if reload.author.id == self.request.user.id or self.request.user.is_superuser:
                title = self.request.POST.get('title')
                lesson = self.request.POST.get('lesson')
                reload.title = title
                reload.lesson = lesson
                reload.save()
                messages.success(self.request, f"Lesson successfully edited ")
        if self.request.POST.get('delete'):
            lesson_obj = Lesson.objects.get(pk=lesson_id)
            lesson_obj.delete()
            messages.success(self.request, f"Lesson successfully deleted ")
        return redirect('/')


class AddLessonView(TemplateView):
    context = {}
    template_name = "lesson/add_lesson.html"

    def post(self, *args, **kwargs):
        if self.request.POST.get('title') and self.request.POST.get('lesson'):
            title = self.request.POST.get('title')
            lesson = self.request.POST.get('lesson')
            Lesson(title=title, lesson=lesson, author_id=self.request.user.id).save()
            messages.success(self.request, f"Lesson successfully added ")
            return redirect('/')


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


def vote(request, lesson_id):
    page = request.POST.get('url')
    try:

        like_obj, created = Like.objects.get_or_create(user_id=request.user.id, lesson_id=lesson_id)
        if created:
            like_obj.like = True
            like_obj.save()
        else:
            like_obj.delete()
    except:
        pass
    return HttpResponseRedirect(reverse('home') + f'?page={page}')


class LessonAPIViewSet(viewsets.ModelViewSet):
    """
    list:
    Retrive all lesson

    '''
    create:
    Add new lesson



    '''
    '''
    read:
    Retrive lesson id

    '''

    '''
    update:
    Update lesson id

    '''
    '''
    partial_update:
    Partial update lesson id

    '''
    '''
    delete:
    Delete lesson id

    '''

    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
