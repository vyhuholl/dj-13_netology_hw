from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from articles.models import Article, Scope, ArticleToScope


class ArticleToScopeInlineFormset(BaseInlineFormSet):

    def clean(self):
        primary_count = sum(
            [form.cleaned_data['primary'] for form in self.forms]
            )
        if primary_count > 1:
            raise ValidationError('Основная категория может быть только одна')
        elif primary_count == 0 and not self.forms[0].is_bound:
            # я решила не выводить ValidationError для пустых форм
            raise ValidationError('Укажите основную категорию')
        return super().clean()


class ArticleToScopeInline(admin.TabularInline):

    model = ArticleToScope
    formset = ArticleToScopeInlineFormset
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    inlines = [ArticleToScopeInline]


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass
