from django.core.management.base import BaseCommand
from user.models import SimpleUser


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--a', action='store_true', help='Deleting all users')
        parser.add_argument('--e', type=str, help='Deleting user with certain email address')

    def handle(self, *args, **kwargs):
        if kwargs['e']:
            try:
                user = SimpleUser.objects.get(email=kwargs['e'])
                user.delete()
            except:
                pass

        if kwargs['a']:
            SimpleUser.objects.all().delete()


