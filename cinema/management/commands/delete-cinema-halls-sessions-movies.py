from django.core.management.base import BaseCommand
from cinema.models import *
from movie.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        halls = Hall.objects.all()
        movies = Movie.objects.all()

        for hall in halls:
            hall.gallery.delete()
            hall.seo.delete()

        halls.delete()

        for movie in movies:
            movie.gallery.delete()
            movie.seo.delete()

        movies.delete()

        cinemas = Cinema.objects.all()

        for cinema in cinemas:
            cinema.gallery.delete()
            cinema.seo.delete()

        cinemas.delete()


