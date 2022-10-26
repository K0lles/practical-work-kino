from django.core.management.base import BaseCommand
from page.models import *


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--a', action='store_true', help='Deleting all pages')

    def handle(self, *args, **kwargs):
        if kwargs['a']:
            try:
                main_page = MainPage.objects.first()
                main_page.seo.delete()
                main_page.delete()

                pages = Page.objects.all()

                for page in pages:
                    page.gallery.delete()
                    page.seo.delete()

                pages.delete()

            except Exception as e:
                pass
