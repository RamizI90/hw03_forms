from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Post(models.Model):
    text = models.TextField(_("Текст"))
    pub_date = models.DateTimeField(_("Дата Публикации"), auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='group'
    )

    def __str__(self):
        # выводим текст поста
        return self.text

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")


class Group(models.Model):
    title = models.CharField(_("Название"), max_length=200)
    slug = models.SlugField(_("Слаг"), max_length=200, unique=True)
    description = models.TextField(_("Описание"))

    class Meta:
        verbose_name = _("Группа")
        verbose_name_plural = _("Группы")

    def __str__(self):
        return self.title
