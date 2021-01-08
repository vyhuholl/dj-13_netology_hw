from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.contrib import admin
from models import Article, Relationship


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        if self.forms[0].is_bound:
            primary_scopes_count = sum(self.forms[0]['primary'])
            if primary_scopes_count > 1:
                raise ValidationError(
            'Основная категория может быть только одна')
            elif primary_scopes_count == 0:
                raise ValidationError('Укажите основную категорию')

        return super().clean()


class RelationshipInline(admin.TabularInline):
    model = Relationship
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]

