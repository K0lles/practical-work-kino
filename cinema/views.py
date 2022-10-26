from django.db.models import Count
from django.shortcuts import render
import importlib

from banner.models import *
from movie.models import *
from page.models import *
from .models import *
settings = importlib.import_module('practical-work-kino.settings')


def header_data(request):
    """Returns data, which will be in the header on each user page"""
    main_page = MainPage.objects.first()
    return {
        'phone_number_first': main_page.phone_number_first if main_page.phone_number_first else '+380500000000',
        'phone_number_second': main_page.phone_number_second if main_page.phone_number_second else '+380500000000',
        }


def home_view(request):
    background_banner = BackgroundBanner.objects.first()
    main_top_banner_photos = MainTopBanner.objects.prefetch_related('maintopbannerphoto_set').first()
    sessions = Session.objects.prefetch_related('movie', 'hall').filter(date__month=timezone.now().month)
    background_photo = None
    news_banner_photos = NewsBanner.objects.prefetch_related('newsbannerphoto_set').first()

    try:
        background_photo = background_banner.photo.url if background_banner.background == 1 else None
    except:
        pass

    context = {
        'title': 'KinoCMS | Головна',
        'background': background_photo,
        'photos': main_top_banner_photos.maintopbannerphoto_set.all() if main_top_banner_photos.turned_on else None,
        'interval': main_top_banner_photos.turning_speed * 1000,
        'sessions': sessions,
        'news_photos': news_banner_photos.newsbannerphoto_set.all() if news_banner_photos.turned_on else None
    }

    # there and further - adding keys with phone numbers
    context.update(header_data(request))

    return render(request, 'cinema/home.html', context=context)


def poster_view(request):
    movies = Movie.objects.filter(session__date__month__gte=timezone.now().month)

    context = {
        'title': 'KinoCMS | Афіша',
        'movies': movies,
    }
    context.update(header_data(request))

    return render(request, 'cinema/poster.html', context=context)


def cinema_view(request):
    cinemas = Cinema.objects.all()

    context = {
        'title': 'KinoCMS | Кінотеатри',
        'cinemas': cinemas
    }
    context.update(header_data(request))

    return render(request, 'cinema/cinema_view.html', context)


def cinema_detail(request, cinema_pk):
    cinema = Cinema.objects.prefetch_related('hall_set',
                                             'hall_set__session_set',
                                             'hall_set__session_set__movie',
                                             'gallery__photo_set').get(pk=cinema_pk)

    context = {
        'title': 'KinoCMS | Огляд кінотеатру',
        'cinema': cinema,
    }
    context.update(header_data(request))

    return render(request, 'cinema/cinema_detail.html', context)


def hall_detail(request, hall_pk):
    hall = Hall.objects.prefetch_related('gallery__photo_set', 'session_set', 'session_set__movie').get(pk=hall_pk)

    context = {
        'title': 'KinoCMS | Зал',
        'hall': hall
    }
    context.update(header_data(request))

    return render(request, 'cinema/hall_detail.html', context)
