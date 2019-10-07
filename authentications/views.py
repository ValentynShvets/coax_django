import jwt
from django.contrib.auth import user_logged_in, authenticate, login
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.serializers import jwt_payload_handler

from Coax import settings
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, viewsets
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, HttpResponse, redirect, render_to_response
from django.template.context_processors import csrf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .forms import SignUpForm
from django.contrib import messages
from .models import *

from authentications.serializers import UserSerializer


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        try:
            print(user['password'])
        except:
            print(user)

        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    except (KeyError, User.DoesNotExist):
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

                messages.success(request, f"Hello, you have successfully registered")
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
                # raw_pass = form.cleaned_data.get('password1')
                login(request, user,  backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f"Welcome {email}")
                return redirect("/")
            else:
                args['login_error'] = "Invalid email or password"
                return render_to_response('lesson/login.html', args)
        else:
            return render_to_response("lesson/login.html", args)
    else:
        return redirect("/")

# def user_login(request):
#     args = {}
#     args.update(csrf(request))
#     if request.POST:
#         email = request.POST.get("email", "")
#         password = request.POST.get("password", "")
#         print(email, password)
#         URL = reverse('token_obtain_pair')
#         print(URL)
#         headers = {
#             'Accept': 'application/json',
#             'Content-Type': 'application/json'
#         }
#         body = {'email': f'{email}', 'password': f'{password}'}
#         resp = requests.request("POST", 'http://127.0.0.1:8000'+URL, data=json.dumps(body), headers=headers)
#         print(resp.json())
#         # user = authenticate(email=email, password=password)
#     else:
#         return render_to_response("lesson/login.html", args)
#     return redirect("/")

def user_logout(request):
    logout(request)
    return redirect("/")


class UserAPIViewSet(viewsets.ModelViewSet):
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
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)


# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)
