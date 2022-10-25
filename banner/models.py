from django.db import models


class MainTopBanner(models.Model):

    class Speed(models.IntegerChoices):
        FIVE_SEC = 5, '5с'
        TEN_SEC = 10, '10с'
        FIFTEEN_SEC = 15, '15с'

    turning_speed = models.IntegerField(choices=Speed.choices, default=5)
    turned_on = models.BooleanField(default=True)


class MainTopBannerPhoto(models.Model):
    main_top_banner = models.ForeignKey(MainTopBanner, on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ImageField(upload_to='banner/main_top_banner/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)


class NewsBanner(models.Model):

    class Speed(models.IntegerChoices):
        FIVE_SEC = 5, '5с'
        TEN_SEC = 10, '10с'
        FIFTEEN_SEC = 15, '15с'

    turning_speed = models.IntegerField(choices=Speed.choices, default=5)
    turned_on = models.BooleanField(default=True)


class NewsBannerPhoto(models.Model):
    news_banner = models.ForeignKey(NewsBanner, on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ImageField(upload_to='banner/news_banner/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)


class BackgroundBanner(models.Model):
    photo = models.ImageField(upload_to='banner/background_banner/')

    class Type(models.IntegerChoices):
        PHOTO_BACKGROUND = 1, 'Фото на фон'
        BACKGROUND = 2, 'Просто фон'

    background = models.IntegerField(choices=Type.choices, default=1)
