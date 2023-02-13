from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор')
)


class User(AbstractUser):

    bio = models.TextField(
        'Биография',
        blank=True,
        help_text='Заполните биографию'
    )

    email = models.EmailField(
        'E-mail',
        unique=True,
        help_text='Введите свой e-mail'
    )

    role = models.CharField(
        'Роль',
        max_length=16,
        choices=ROLE_CHOICES,
        default=ROLE_CHOICES[0][0],
        help_text='Выберите роль пользователя'
    )

    @property
    def is_moderator(self):
        if self.role == ROLE_CHOICES[1][0]:
            return True
        return False

    @property
    def is_admin(self):
        if self.role == ROLE_CHOICES[2][0]:
            return True
        return False

    def __str__(self):
        return self.username
