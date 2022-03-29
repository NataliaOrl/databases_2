from django.contrib import admin

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, ArticleTag, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


class ArticleTagInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main = False
        for form in self.forms:
            new_main = form.cleaned_data.get('is_main')
            if not is_main and new_main:
                is_main = True
                continue
            elif not new_main:
                continue
            elif is_main and new_main:
                raise ValidationError('Основным может быть только один раздел')
        if not is_main:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    formset = ArticleTagInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [ArticleTagInline]
