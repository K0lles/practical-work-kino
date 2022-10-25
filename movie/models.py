from django.db import models
from cinema.models import Gallery, SEO, Hall


class Movie(models.Model):
    name = models.CharField(max_length=55, verbose_name='Назва фільма')
    description = models.TextField(verbose_name='Опис')
    main_photo = models.ImageField(upload_to='movie/', verbose_name='Головна картинка')
    gallery = models.OneToOneField(Gallery, on_delete=models.CASCADE, verbose_name='Галерея картинок', blank=True,
                                   null=True)
    trailer_url = models.URLField(verbose_name='Посилання на трейлер')
    type_2D = models.BooleanField(default=True)
    type_3D = models.BooleanField(default=True)
    type_IMAX = models.BooleanField(default=True)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, blank=True, null=True)


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    class Type(models.TextChoices):
        type_2D = '2D', '2D'
        type_3D = '3D', '3D'

    type = models.CharField(max_length=10, choices=Type.choices, verbose_name='Тип')
    type_IMAX = models.BooleanField(default=False)
    price = models.FloatField()
    date = models.DateTimeField()
