"""Coax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework_simplejwt import views as jwt_views

from django.contrib import admin


schema_view = get_schema_view(
    openapi.Info(
        title='My API title',
        default_version='v1',
        description= "Description",
        contact= openapi.Contact(email='valentynshvets@icloud.com'),
        license= openapi.License(name='BBD'),

    )
)

api_patterns = [

    path('lessons/', include('lesson.urls')),

]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
    path('', include('authentications.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]

# urlpatterns += [
#     # Your URLs...
#     path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
# ]
#
# urlpatterns += [
#     path('admin/', admin.site.urls),
# ]
