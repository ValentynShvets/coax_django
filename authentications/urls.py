from django.urls import path, include

from .views import CreateUserAPIView, UserRetrieveUpdateAPIView
from .views import user_login,user_logout,registration,CreateUserAPIView, MainView
app_name = 'authentications'
urlpatterns = [
    # path('', MainView.as_view(), name= 'home'),
    # path('', include('lesson.urls')),
    path('create/', CreateUserAPIView.as_view()),
    path('login/', user_login, name='login'),
    path('loguot/', user_logout, name='logout'),
    path('signup/', registration, name='signup'),

]


urlpatterns += [

    path('update/', UserRetrieveUpdateAPIView.as_view()),
]