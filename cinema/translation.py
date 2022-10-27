from modeltranslation.translator import register, TranslationOptions
from .models import Cinema, Hall


@register(Cinema)
class CinemaTranslationOption(TranslationOptions):
    fields = ('name', 'description', 'condition')


@register(Hall)
class HallTranslationOption(TranslationOptions):
    fields = ('description', )
