from enum import Enum

from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from users.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class UserRoles(Enum):
    # TODO закончите enum-класс для пользователя
    USER = ('user', 'пользователь')
    ADMIN = ('admin', 'администратор')


class User(AbstractBaseUser):
    # TODO переопределение пользователя.
    # TODO подробности также можно поискать в рекоммендациях к проекту
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = PhoneNumberField()
    image = models.ImageField(upload_to='avatars/')
    role = models.CharField(
        max_length=5,
        choices=[i.value for i in UserRoles],
        default=UserRoles.USER.value[0]
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'role']

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN.value

    @property
    def is_user(self):
        return self.role == UserRoles.USER.value




