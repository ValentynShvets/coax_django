from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.settings import api_settings

from authentications.models import User


class BaseAPITest(APITestCase):

    def create(self, email='test@gmail.com', password='fssad1997'):
        user = User.objects.create_superuser(email=email, password=password)
        user.is_active = True
        user.save()

        return user

    def create_and_login(self, email='test@gmail.com', password='fssad1997'):
        user = self.create(email=email, password=password)
        self.authorize(user)
        return user

    def authorize(self, user, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"{api_settings.AUTH_HEADER_TYPES[0]} {token}",
            **additional_headers
        )

    def logout(self, **additional_headers):
        self.client.credentials(**additional_headers)
