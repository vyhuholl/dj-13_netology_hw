from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(
        null=True, blank=True, verbose_name='Изображение'
        )
    scopes = models.ManyToManyField('Scope', through='ArticleToScope')

    class Meta:

        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Scope(models.Model):

    scope = models.CharField(max_length=25, unique=True, verbose_name='Раздел')

    class Meta:

        verbose_name = 'Тематика Статьи'
        verbose_name_plural = 'Тематика Статьи'

    def __str__(self):
        return self.scope


class ArticleToScope(models.Model):

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='articles'
        )
    scope = models.ForeignKey(
        Scope, on_delete=models.CASCADE, related_name='scopes'
        )
    primary = models.BooleanField()

    class Meta:
        ordering = ['-primary', 'scope__scope']
