from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import status, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import *

from django.contrib import messages
from .models import *


class MainView(TemplateView):
    context = {}
    template_name = "lesson/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        # context['cash'] = balance(self.request)
        return context


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class LessonAPIViewSet(viewsets.ModelViewSet):
    """
    list:
    Retrive all lesson

    '''
    json{
    "title": "lll;"

    }

    '''



    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,)


class LessonApiViews(APIView):
    def get(self, *args, **kwargs):
        instances = Lesson.objects.all()
        ser = LessonSerializer(instances, many=True)

        return Response(data=ser.data)

    def post(self, *args, **kwargs):
        ser = LessonSerializer(data=self.request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(data=ser.data, status=status.HTTP_201_CREATED)


# def vote(request, lesson_id):
#     question = get_object_or_404(Lesson, pk=lesson_id)
#     if request.POST.get('choice'):
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#         selected_choice.votes += 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('polls:details', args=(question.id,)))
#
#     elif request.POST.get('minus'):
#         selected_choice = question.choice_set.get(pk=request.POST['minus'])
#         selected_choice.votes -= 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('polls:details', args=(question.id,)))
