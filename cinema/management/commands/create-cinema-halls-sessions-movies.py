import datetime

from django.core.management.base import BaseCommand
from cinema.models import *
from movie.models import *
from random import choice, randrange


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        if not Cinema.objects.exists():
            gallery = Gallery.objects.create(name='Cinemary')

            for index in range(0, 3):
                Photo.objects.create(photo=f'static_preload/preload_cinema/gallery/{index}.jpg',
                                     gallery=gallery)

            seo = SEO.objects.create(url='https://cinemary.com',
                                     title='Cinemary',
                                     keyword='Cinemary, Cinemary cinema',
                                     seo_description='Cinemary, the cinema with comfortable conditions')

            cinema = Cinema.objects.create(name='Cinemary',
                                           description='Cinemary with peaceful atmosphere',
                                           condition='Big spacious halls with comfortable seats',
                                           logo='static_preload/preload_cinema/logo.jpg',
                                           banner_photo='static_preload/preload_cinema/banner-photo.jpg',
                                           gallery=gallery,
                                           seo=seo)

            for index in range(0, 4):
                gallery = Gallery.objects.create(name=f'Hall {index + 1}')

                seo = SEO.objects.create(url=f'https://hall-{index + 1}.com',
                                         title=f'Hall {index + 1}',
                                         keyword=f'Hall {index + 1}, Cinema hall',
                                         seo_description='Hall seo description')

                for photo_index in range(0, 2):
                    Photo.objects.create(photo=f'static_preload/preload_halls/gallery-{photo_index}/{photo_index}.jpg',
                                         gallery=gallery)

                Hall.objects.create(cinema_id=cinema,
                                    number=index + 1,
                                    description='Hall very comfortable',
                                    scheme=f'static_preload/preload_halls/scheme-{index}.jpg',
                                    banner_photo=f'static_preload/preload_halls/banner-photo-{index}.jpg',
                                    gallery=gallery,
                                    seo=seo)
            for hall_number in range(1, 4):
                hall = Hall.objects.get(number=hall_number)
                for index, name_tuple in enumerate([('hatiko', 'Хатіко', 'https://www.youtube.com/embed/nRiYwfZ-5qA?autoplay=1&mute=1'),
                                                    ('lost-city', 'Загублене місто', 'https://www.youtube.com/embed/P3C1nNnaMgY?autoplay=1&mute=1'),
                                                    ('joker', 'Джокер', 'https://www.youtube.com/embed/q3IqAuTlTfA?autoplay=1&mute=1'),
                                                    ('jumanji', 'Джуманджі', 'https://www.youtube.com/embed/ImZCLnCXglI?autoplay=1&mute=1'),
                                                    ('escape-from-shoushenko', 'Втеча з Шоушенко', 'https://www.youtube.com/embed/kgAeKpAPOYk?autoplay=1&mute=1'),
                                                    ('christ-parent', 'Хрещений батько', 'https://www.youtube.com/embed/ar1SHxgeZUc?autoplay=1&mute=1')]):
                    gallery = Gallery.objects.create(name=name_tuple[0])
                    seo = SEO.objects.create(url=f'https://movie-{name_tuple[0]}.com',
                                             title=name_tuple[0],
                                             keyword=f'{name_tuple[0]}, {name_tuple[1]}',
                                             seo_description=f'Description movie {name_tuple[1]}')

                    for inner_index in range(0, 3):
                        Photo.objects.create(photo=f'static_preload/preload_movies/movie_{index}/gallery/{inner_index}.jpg',
                                             gallery=gallery)

                    type_2D = choice([True, False])
                    type_3D = True if not type_2D else False
                    type_IMAX = choice([True, False])
                    movie = Movie.objects.create(name=name_tuple[1],
                                                 description=f'{name_tuple[1]} description movie',
                                                 main_photo=f'static_preload/preload_movies/movie_{index}/{name_tuple[0]}.jpg',
                                                 gallery=gallery,
                                                 trailer_url=name_tuple[2],
                                                 type_2D=type_2D,
                                                 type_3D=type_3D,
                                                 type_IMAX=type_IMAX,
                                                 seo=seo
                                                 )
                    Session.objects.create(movie=movie,
                                           hall=hall,
                                           type='2D' if movie.type_2D else '3D',
                                           type_IMAX=movie.type_IMAX,
                                           price=choice([150.0, 190.0, 210.0, 180.0]),
                                           date=datetime.datetime(2022,
                                                                  10,
                                                                  randrange(20, 31),
                                                                  randrange(10, 22),
                                                                  choice([0, 30])))
