import uuid as uuid_lib

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, UserManager)
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(RegexValidator):
    regex = r'^\w+$'
    message = "英数字と'_'のみが使用できます。"
    flags = 0


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_data):
        email = self.normalize_email(email)
        user = self.model(self, email=email, **extra_data)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staff(self, email, password, **extra_data):
        extra_data.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_data)

    def create_superuser(self, email, password, **extra_data):
        extra_data.setdefault('is_staff', True)
        extra_data.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_data)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField('uuid', default=uuid_lib.uuid4, primary_key=True, editable=False)

    username_validator = UsernameValidator()

    username = models.CharField(
        'Username',
        max_length=30,
        unique=True,
        help_text="ユーザー名は4~30文字の英数字と'_'が使用できます",
        validators=[
            username_validator, MinLengthValidator(4)
        ],
        error_messages={
            'unique': 'このユーザー名は既に使用されています',
        }
    )

    objects = UserManager()

    email = models.EmailField(blank=True)

    date_joined = models.DateTimeField(default=timezone.now(), editable=False)

    date_started = models.DateTimeField('CTF開始時間', blank=True, null=True, editable=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    is_staff = models.BooleanField(
        default=False,
        help_text='管理サイトにログインできるかを指定します。',
    )
    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
