import uuid

from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def sending_mail(username, email, password):
    send_mail(
        'Progect YaMBT - It`s your confirmation code',
        f'Добрый день, {username}, Вот ваш код подтверждения {password}',
        None,
        [email],
        fail_silently=False,
    )


def password_generator():
    return str(uuid.uuid4())


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'token': str(refresh.access_token)}
