from django.urls import path

from .views import user_login,user_logout,registration,CreateUserAPIView, MainView
app_name = 'authentications'
urlpatterns = [
    path('', MainView.as_view(), name= 'home'),
    path('create/', CreateUserAPIView.as_view()),
    path('login/', user_login, name='login'),
    path('loguot/', user_logout, name='logout'),
    path('signup/', registration, name='signup'),

]

from .views import CreateUserAPIView, UserRetrieveUpdateAPIView

urlpatterns += [

    path('update/', UserRetrieveUpdateAPIView.as_view()),
]