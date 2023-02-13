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
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        "Текст комментария",
        help_text="Введите текст комментария"
    )
    created = models.DateTimeField(
        "Дата публикации комментария",
        auto_now_add=True
    )
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=None, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
