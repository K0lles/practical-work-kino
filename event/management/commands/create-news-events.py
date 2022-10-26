from django.core.management.base import BaseCommand

from event.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        for index in range(0, 2):
            gallery = Gallery.objects.create()
            seo = SEO.objects.create(
                url=f'https://some{index}.com',
                title='Title',
                keyword='Keyword',
                seo_description='SEO'
            )
            Event.objects.create(
                name='Подія 1',
                description='Опис події 1',
                logo=f'static_preload/preload_news/{index}.jpg',
                type='event',
                status=True,
                gallery=gallery,
                url='https://youtube.com',
                seo=seo
            )

        for index in range(0, 2):
            gallery = Gallery.objects.create()
            seo = SEO.objects.create(
                url=f'https://some{index}.com',
                title='Title',
                keyword='Keyword',
                seo_description='SEO'
            )
            Event.objects.create(
                name='Новина 1',
                description='Опис новини 1',
                logo=f'static_preload/preload_news/{index}.jpg',
                type='news',
                status=True,
                gallery=gallery,
                url='https://youtube.com',
                seo=seo
            )
