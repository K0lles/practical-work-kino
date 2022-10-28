from django.core.management.base import BaseCommand

from banner.models import *
from page.models import MainPage
from cinema.models import SEO


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not MainTopBanner.objects.exists():
            main_top_banner = MainTopBanner.objects.create(turning_speed=5,
                                                           turned_on=True)

            for index in range(0, 3):
                MainTopBannerPhoto.objects.create(main_top_banner=main_top_banner,
                                                  photo=f'static_preload/preload_banners/main_top_banners/{index}.jpg',
                                                  url=f'https://photo-{index + 1}-.photo',
                                                  text=f'Text of {index + 1} photo')

        if not NewsBanner.objects.exists():
            news_banner = NewsBanner.objects.create(turning_speed=5,
                                                    turned_on=True)

            for index in range(0, 3):
                NewsBannerPhoto.objects.create(news_banner=news_banner,
                                               photo=f'static_preload/preload_banners/news_banners/{index}.jpg',
                                               url=f'https://photo{index}.com')

        if BackgroundBanner.objects.exists():
            background_banner = BackgroundBanner.objects.create(photo='static_preload/preload_banners/background_banner/background_banner.jpg',
                                                                background=1)

        if MainPage.objects.exists():
            seo = SEO.objects.create(url='https://main-page.com',
                                     title='Main Page Seo',
                                     keyword='MainPage',
                                     seo_description='Description in seo of main page')

            MainPage.objects.create(phone_number_first='+380991111111',
                                    phone_number_second='+380509999999',
                                    status=True,
                                    seo_text='This is main page, okey',
                                    seo=seo)
