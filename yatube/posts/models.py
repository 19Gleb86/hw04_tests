from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        "Название",
        max_length=200,
        help_text="Название группы (не более 200 символов)"
    )
    slug = models.SlugField(
        "Слаг",
        unique=True,
        help_text="Название группы в поисковой строке"
    )
    description = models.TextField(
        "Описание",
        help_text="Описание группы"
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        "Текст",
        help_text="Содержание поста"
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
        help_text="Дата публикации поста (указывается автоматически)"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор"
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='group',
        verbose_name="Группа"
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]
