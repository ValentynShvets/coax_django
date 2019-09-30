from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, admin, is_staff, is_superuser, **extra_fields):
        # now = timezone.now()
        if not email:
            raise ValueError('email must be set')
        email = self.normalize_email(email)
        user = User(email=email,
                    admin=admin, is_staff=is_staff, is_superuser=is_superuser,
                    **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # id = models.IntegerField(primary_key=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # objects = UserManager()
    objects = CustomUserManager()

    def __str__(self):
        return self.email
