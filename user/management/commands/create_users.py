from django.core.management.base import BaseCommand
from user.models import SimpleUser
import datetime
from django.utils.crypto import get_random_string
from random import choices, randrange


class Command(BaseCommand):
    help = 'Creates users'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int, help='Amount of users to add')

    def handle(self, *args, **kwargs):
        amount = kwargs['amount']
        if not SimpleUser.objects.exists():
            SimpleUser.objects.create_superuser(email='superuser@gmail.com',
                                                password='123qweasd',
                                                name='Superuser',
                                                surname='Surname',
                                                alias='superuser-from-command',
                                                card_number=654789,
                                                language='ukrainian',
                                                sex='male',
                                                birthday=datetime.datetime(2005, 5, 25),
                                                phone_number='+380990637128',
                                                city='Chernivtsi')

            for number in range(amount):
                SimpleUser.objects.create_user(email=f'test{number}@gmail.com',
                                               password='123qweasd',
                                               name=get_random_string(8),
                                               surname='Surname',
                                               alias=f'{get_random_string(8)}-from-command',
                                               card_number=654789,
                                               language='ukrainian',
                                               sex=choices(['female', 'male'])[0],
                                               birthday=datetime.datetime(randrange(1972, 2010),
                                                                          randrange(1, 12),
                                                                          randrange(1, 30)),
                                               phone_number='+380990637128',
                                               city=choices(['Chernivsti', 'Lviv', 'Dnipro', 'Odesa', 'Kyiv'])[0])
