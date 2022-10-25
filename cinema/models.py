from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Cinema(models.Model):
    name = models.CharField(max_length=55, verbose_name='Назва кінотеатру')
    description = models.TextField(verbose_name='Опис')
    condition = models.TextField(verbose_name='Умови')
    logo = models.ImageField(upload_to='cinema/cinema/logo/', verbose_name='Логотип')
    banner_photo = models.ImageField(upload_to='cinema/cinema/banner_photo/', verbose_name='Фото верхнього баннера')
    gallery = models.OneToOneField('Gallery', on_delete=models.CASCADE, verbose_name='Галерея картинок',
                                   blank=True, null=True)
    seo = models.ForeignKey('SEO', on_delete=models.CASCADE, verbose_name='SEO блок', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Кінотеатри'

    def __str__(self):
        return self.name


class Hall(models.Model):
    cinema_id = models.ForeignKey(Cinema, on_delete=models.CASCADE, verbose_name='Кінотеатр', blank=True, null=True)
    number = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Номер зала')
    description = models.TextField(verbose_name='Опис залу', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата створення', blank=True)
    scheme = models.ImageField(upload_to='cinema/hall/scheme/', verbose_name='Схема зала')
    banner_photo = models.ImageField(upload_to='cinema/hall/banner_photo/', verbose_name='Верхній баннер')
    gallery = models.OneToOneField('Gallery', on_delete=models.CASCADE, verbose_name='Галерея картинок', blank=True, null=True)
    row_amount = models.IntegerField(default=6, validators=[MinValueValidator(1)], blank=True)
    seat_amount = models.IntegerField(default=12, validators=[MinValueValidator(1)], blank=True)
    seo = models.ForeignKey('SEO', on_delete=models.CASCADE, verbose_name='SEO блок', blank=True, null=True)

    def __str__(self):
        return f"Hall {self.number}"


class Gallery(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class Photo(models.Model):
    photo = models.ImageField(upload_to='gallery/')
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.photo.url


class SEO(models.Model):
    url = models.URLField(verbose_name='Url')
    title = models.CharField(max_length=55, verbose_name='Title')
    keyword = models.CharField(max_length=155, verbose_name='Keywords')
    seo_description = models.TextField(verbose_name='Description', blank=True)

    def __str__(self):
        return self.title
