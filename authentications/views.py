import jwt
from django.contrib.auth import user_logged_in, authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_jwt.serializers import jwt_payload_handler

from Coax import settings
from authentications.forms import SignUpForm
from lesson.models import Lesson
from .models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, HttpResponse, redirect, render_to_response
from django.template.context_processors import csrf
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import *

# from COAX_BOOTCAMP.bootcamp.lesson.serializers import LessonSerializer
from .forms import SignUpForm
from django.contrib import messages
from .models import *

#
from authentications.serializers import UserSerializer


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        print(user)
        try:
            print(user['password'])
        except:
            print(user)
        # user['password'] = "f"
        # print(user['password'])
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MainView(TemplateView):
    context = {}
    template_name = "lesson/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(data=Lesson.objects.all(), **kwargs)
        # context['data'] = Lesson.objects.all()
        print(context)
        # context['cash'] = balance(self.request)
        return context


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)


def registration(request):
    if not request.user.id:
        args = {}
        args.update(csrf(request))
        args['form'] = SignUpForm()
        if request.POST:
            newuser_form = SignUpForm(request.POST)
            if newuser_form.is_valid():
                newuser_form.save()
                newuser = authenticate(email=newuser_form.cleaned_data['email'],
                                       password=newuser_form.cleaned_data['password2'], )
                login(request, newuser)

                messages.success(request, f"Вітаємо, {request.POST.get('first_name', '')} Ви успішно зареєструвались")
                return redirect("/")
            else:
                args['form'] = newuser_form
        return render_to_response("lesson/signup.html", args)
    else:
        return redirect("/")


def user_login(request):
    if not request.user.id:
        args = {}
        args.update(csrf(request))
        if request.POST:
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Ви успішно ввійшли")
                return redirect("/")
            else:
                args['login_error'] = "Невірний email або пароль"
                return render_to_response('lesson/login.html', args)
        else:
            return render_to_response("lesson/login.html", args)
    else:
        return redirect("/")


def user_logout(request):
    logout(request)
    return redirect("/")

# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)
