from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count

from core.models import PublishedModel


User = get_user_model()


class Category(PublishedModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы латиницы,'
                  ' цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class PostQuerySet(models.QuerySet):

    def count_comments(self):
        return self.annotate(
            comment_count=Count('комментарий'))

    def related_data(self):
        return self.select_related(
            'category', 'location', 'author')

    def base_filters(self):
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__date__lte=datetime.now()
        ).order_by('-pub_date').count_comments()

    def post_filter(self):
        return self.related_data().count_comments()


class PostManager(models.Manager):

    def get_posts_qs(self):
        return (
            PostQuerySet(self.model)
            .related_data()
            .base_filters()
            .count_comments()
        )


class Post(PublishedModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок')
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем'
                  ' — можно делать отложенные публикации.',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор записи',
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        Location,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='blog_images',
        blank=True,
        help_text='Любая картинка и желательно в тему поста')
    objects = PostQuerySet.as_manager()
    published = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    text = models.TextField('Текст комментария', null=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='комментарий',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('created_at',)
