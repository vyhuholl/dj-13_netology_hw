from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(
        null=True, blank=True, verbose_name='Изображение'
        )
    scopes = models.ManyToManyField(
        'Scope', through='ArticleToScope', related_name='scopes'
        )

    class Meta:

        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Scope(models.Model):

    topic = models.CharField(
        max_length=25, unique=True, verbose_name='Название'
        )

    class Meta:

        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['topic']

    def __str__(self):
        return self.topic


class ArticleToScope(models.Model):

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='as_articles'
        )
    scope = models.ForeignKey(
        Scope, on_delete=models.CASCADE, related_name='as_scopes',
        verbose_name='Раздел'
        )
    is_main = models.BooleanField(verbose_name='Основной')

    class Meta:

        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'
        ordering = ['-is_main', 'scope__topic']
