from django.db import models


class ArticleScope(models.Model):

    scope = models.CharField(max_length=25, verbose_name='Раздел')

    class Meta:
        verbose_name = 'Тематика Статьи'
        verbose_name_plural = 'Тематики Статьи'

    def __str__(self):
        return self.scope


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, verbose_name='Изображение')
    scopes = models.ManyToManyField(
        ArticleScope, through='Relationship',
        through_fields=('scope', 'primary')
        )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Relationship(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    scope = models.ForeignKey(ArticleScope, on_delete=models.CASCADE)
    primary = models.BooleanField(verbose_name='Основной')

    class Meta:
        ordering = ['-primary', 'scope__name']

    def __str__(self):
        return f'{self.article}_{self.scope}'
