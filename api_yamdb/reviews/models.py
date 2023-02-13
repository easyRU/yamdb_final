from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validator import validate_year

NAME_MAX_LENGTH = 200
SLUG_MAX_LENGTH = 50


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Строка идентификатор',
        unique=True,
        max_length=SLUG_MAX_LENGTH
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории',
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Строка идентификатор',
        unique=True,
        max_length=SLUG_MAX_LENGTH
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры',
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=NAME_MAX_LENGTH
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='TitleAndGenre'
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=[validate_year]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


class TitleAndGenre(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Произведение - {self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Автор отзыва'
    )
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Произведение',
        related_name='reviews',
        help_text='Произведение на которое написан отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True,
        help_text='Дата публикации отзыва'
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        help_text='Введдите оценку'
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='only_one_review'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор комментария'
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Отзыв',
        related_name='comments',
        help_text='Отзыв, к которому написан комментарий'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        db_index=True,
        auto_now_add=True,
        help_text='Дата публикации комментария'
    )

    class Meta:
        ordering = ['-pub_date']
