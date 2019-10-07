from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    # def create_user(self, email, password):
    #     """Creates and saves a User with the given email, date of
    #     birth and password.
    #     """
    #     if not email:
    #         raise ValueError(_('Users must have an email address'))
    #
    #     user = self.model(
    #         email=self.normalize_email(email),
    #     )
    #
    #     user.set_password(password)
    #     user.save()
    #     return user
    #
    # def create_superuser(self, email,password):
    #     """Creates and saves a superuser with the given email, date of
    #     birth and password.
    #     """
    #     user = self.create_user(
    #         email,
    #         password,
    #     )
    #
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.is_active = True
    #     user.save()
    #     return user
    def _create_user(self, email, password, is_staff, is_superuser, is_active, **extra_fields):
        if not email:
            raise ValueError('email must be set')
        email = self.normalize_email(email)
        user = User(email=email,
                    is_staff=is_staff, is_superuser=is_superuser, is_active=is_active,
                    **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, True, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)

    is_staff = models.BooleanField(default=False,
                                   help_text='Designates whether this user can access this admin site.',
                                   verbose_name='is staff')
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.',
        verbose_name='is active'
    )
    is_superuser = models.BooleanField(default=False,
                                       help_text='Designates that this user has all permissions without '
                                                 'explicitly assigning them.',
                                       verbose_name='is superuser')

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.id}, {self.email}"

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_staff:
            return True

        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return self.is_staff

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
