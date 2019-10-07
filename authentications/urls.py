from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UserRetrieveUpdateAPIView
from .views import user_login, user_logout, registration, CreateUserAPIView

app_name = 'authentications'
# router = SimpleRouter()
# router.register('', UserAPIViewSet , base_name='users')

urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('login/', user_login, name='login'),
    path('loguot/', user_logout, name='logout'),
    path('signup/', registration, name='signup'),

]

urlpatterns += [

    path('update/', UserRetrieveUpdateAPIView.as_view()),
]
