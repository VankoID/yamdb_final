from django.db import models
from users.models import CustomUser

from .validators import year_validator


class Category(models.Model):
    """
    Категории (типы) произведений.
    Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
    Список категорий (Category) может быть расширен администратором.
    """
    name = models.CharField(
        'Название категории',
        max_length=256,
        db_index=True
    )
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Жанр произведения.
    Произведению может быть присвоен жанр (Genre)
    из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
    Новые жанры может создавать только администратор.
    """
    name = models.CharField('Название жанра', max_length=150, db_index=True)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Конкретное произведение, к которому можно оставлять отзывы (Reviews).
    Например, книга, фильм, музыкальный альбом или игра.
    """
    name = models.CharField('Название произведения', max_length=200)
    year = models.PositiveSmallIntegerField(
        'Год выпуска произведения',
        validators=[year_validator],
    )
    description = models.CharField(
        'Описание произведения',
        max_length=500,
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Отзыв о конкретном произведении.
    Отзыв может быть оставлен пользователем или администратором.
    """
    SCORE_CHOICES = (
        (1, '1. Неудовлетворительно'),
        (2, '2. Почти удовлетворительно'),
        (3, '3. Удовлетворительно'),
        (4, '4. Весьма удовлетворительно'),
        (5, '5. Хорошо'),
        (6, '6. Весьма хорошо'),
        (7, '7. Очень хорошо'),
        (8, '8. Почти отлично'),
        (9, '9. Отлично'),
        (10, '10. Превосходно'),
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва', max_length=10000)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        choices=SCORE_CHOICES
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        """Пользователь может оставить только один отзыв на произведение."""
        constraints = [
            models.UniqueConstraint(
                name='unique_review',
                fields=['title', 'author'],
            )]
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Комментарий к отзыву (Review).
    Пользователи могут оставлять комментарии, редактировать
    и удалять свои собственные. Модераторы и администраторы
    имеют полные права на редактирование и удаление комментариев.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField('Текст комментария', max_length=1000)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария', auto_now_add=True
    )

    class Meta:
        ordering = ('review', '-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
