from modeltranslation.translator import register, TranslationOptions
from .models import Movie


@register(Movie)
class MovieTranslationOption(TranslationOptions):
    fields = ('name', 'description',)
