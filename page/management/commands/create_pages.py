from django.core.management.base import BaseCommand
from page.models import *
from cinema.models import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        if not MainPage.objects.first():
            seo = SEO.objects.create(url='https://main-page.com',
                                     title='Main Page',
                                     keyword='MainPage, MainPageKeyword',
                                     seo_description='Main Page')

            MainPage.objects.create(phone_number_first='+380509795648',
                                    phone_number_second='+38066974578',
                                    seo_text='Main page was created',
                                    seo=seo)

        types = ['about_cinema', 'cafe_bar', 'vip_hall', 'baby_room', 'advertisment']
        for index, name in enumerate(['Про кінотеатр', 'Кафе-бар', 'Vip-зал', 'Дитяча кімната', 'Реклама']):
            if not Page.objects.filter(type=name).exists():
                seo = SEO.objects.create(url='https://pages.com',
                                         title=name,
                                         keyword=f'{name}, {name} page',
                                         seo_description=f'{name} description')
                gallery = Gallery.objects.create(name=name)
                for inner_index in range(0, 3):
                    Photo.objects.create(photo=f'static_preload/preload_pages/gallery_{index}/{inner_index}.jpg',
                                         gallery=gallery)
                Page.objects.create(name=name,
                                    description=f'{name} description',
                                    main_photo=f'static_preload/preload_pages/{index}.jpg',
                                    gallery=gallery,
                                    seo=seo,
                                    type=types[index]
                                    )


