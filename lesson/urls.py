from django.urls import path, include
from rest_framework.routers import SimpleRouter
from Coax.urls import *
from . import views

app_name = 'lesson'
router = SimpleRouter()
router.register('', views.LessonAPIViewSet, base_name='hello')
urlpatterns = [

    path('get/',views.LessonApiViews.as_view(), name='article'),
    path('', views.MainView.as_view(), name='home'),
    # path('page/', views.PageView.as_view(), name='page'),
    # path('login/', views.user_login, name='login'),
    # path('loguot/', views.user_logout, name='logout'),
    # path('signup/', views.registration, name='signup'),
    # path('change/', views.user_change_password, name='change'),
]+router.urls
# urlpatterns += [
#     # path('hello/', views.HelloView.as_view(), name='hello'),
#     path('api/', include(api_patterns)),
#
# ]+router.urls

base_urlpatterns = [
    path('', views.HelloView.as_view(), name='home'),

]