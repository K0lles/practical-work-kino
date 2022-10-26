from django.db import models
from django.utils import timezone

from cinema.models import Gallery, SEO


class Event(models.Model):
    name = models.CharField(max_length=55, verbose_name='Назва')
    description = models.TextField(verbose_name='Опис')
    created_at = models.DateField(default=timezone.now, verbose_name='Дата створення')
    logo = models.ImageField(upload_to='event/logo/', verbose_name='Головна картинка')

    class Types(models.TextChoices):
        news = 'news', 'News'
        event = 'event', 'Event'

    type = models.CharField(max_length=55, choices=Types.choices, blank=True, null=True)
    status = models.BooleanField(default=True)
    gallery = models.ForeignKey(Gallery, verbose_name='Галерея картинок', on_delete=models.CASCADE)
    url = models.URLField(verbose_name='Посилання на відео')
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, blank=True, null=True)