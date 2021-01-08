from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet
from articles.models import Article, Scope, ArticleToScope


class ArticleToScopeInlineFormset(BaseInlineFormSet):

    def clean(self):
        primary_count = [
            form.cleaned_data['is_main'] for form in self.forms
            ].count(True)
        if primary_count == 0 and self.forms:
            # я решила не выводить ошибку для статей без тэгов,
            # по условию, они не запрещены
            raise ValidationError('Укажите основную категорию')
        elif primary_count > 1:
            raise ValidationError('Основная категория может быть только одна')
        return super().clean()


class ArticleToScopeInline(admin.TabularInline):

    model = ArticleToScope
    formset = ArticleToScopeInlineFormset
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    inlines = [ArticleToScopeInline]
    ordering = ['-published_at']


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass
