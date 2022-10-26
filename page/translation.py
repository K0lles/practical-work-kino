from modeltranslation.translator import register, TranslationOptions
from .models import Page


@register(Page)
class PageTranslationOption(TranslationOptions):
    fields = ('name', 'description')
