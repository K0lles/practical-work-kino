from modeltranslation.translator import register, TranslationOptions
from .models import Event


@register(Event)
class EventTranslationOption(TranslationOptions):
    fields = ('name', 'description',)
