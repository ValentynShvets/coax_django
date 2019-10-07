from django.urls import path, include
from rest_framework.routers import SimpleRouter
from Coax.urls import *
from . import views

app_name = 'lesson'
router = SimpleRouter()
router.register('', views.LessonAPIViewSet, base_name='lessons')
urlpatterns = [

              ] + router.urls

base_patterns = [

    # path('lessons/', views.LessonAPIViewSet.as_view({'get': 'list'}), name='lessons'),

]
