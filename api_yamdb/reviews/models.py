from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    RegexValidator)
from django.db import models
from users.models import User

from .validators import validate_year


class Category(models.Model):
    """Модель категории произведения"""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор категории',
        max_length=50,
        unique=True,
        validators=(RegexValidator(r'^[-a-zA-Z0-9_]+$'),)
    )

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Модель жанра произведения"""
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256
    )

    slug = models.SlugField(
        verbose_name='Идентификатор жанра',
        max_length=50,
        unique=True,
        validators=(RegexValidator(r'^[-a-zA-Z0-9_]+$'),)
    )

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения"""
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )

    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=(validate_year,)
    )

    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True
    )

    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )

    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения',
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.name


class Review(models.Model):
    """Модель отзыва на произведение."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        related_name='reviews',
        on_delete=models.CASCADE,
        null=True
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        related_name='reviews',
        on_delete=models.CASCADE,
        null=True
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10),
        )
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='Каждый автор может написать только один отзыв'
            ),
        )

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.text[:30]


class Comment(models.Model):
    """Модель комментария на отзыв."""
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        related_name='comments',
        on_delete=models.CASCADE,
        null=True
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        related_name='comments',
        on_delete=models.CASCADE,
        null=True
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        related_name='comments',
        on_delete=models.CASCADE,
        null=True
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.text[:30]
