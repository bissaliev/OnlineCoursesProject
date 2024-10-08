from django.conf import settings
from django.db import models


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name="Автор",
    )
    title = models.CharField(
        max_length=250,
        verbose_name="Название",
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Дата и время начала курса",
    )
    price = models.PositiveBigIntegerField(verbose_name="Стоимость курса")
    available = models.BooleanField(default=False, verbose_name="Доступен")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ("-id",)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name="Название",
    )
    link = models.URLField(
        max_length=250,
        verbose_name="Ссылка",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ("id",)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(
        max_length=250,
        verbose_name="Название группы",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="groups",
        verbose_name="Курс",
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="group_students",
        verbose_name="Студенты",
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ("-id",)
