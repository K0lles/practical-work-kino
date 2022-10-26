from django.db.models import Count
from django.shortcuts import render, redirect

from admin_cms.forms import main_top_banner_form_factory, main_top_formset_factory, background_banner_form_factory, \
    news_banner_form_factory, news_banner_formset_factory
from banner.models import MainTopBanner, BackgroundBanner, NewsBanner, MainTopBannerPhoto, NewsBannerPhoto
from cinema.models import Cinema
from user.models import SimpleUser
from movie.models import *


def statistics_view(request):

    # first chart with sex
    sex_groups = SimpleUser.objects.all().values('sex').annotate(cnt=Count('sex')).order_by('sex')
    males = sex_groups[1]['cnt']
    females = sex_groups[0]['cnt']

    # sessions sorted and counted by dates
    groups = Session.objects.all().values('date__date').annotate(cnt=Count('date__date')).order_by('date__date')
    session_dates = [f"{group['date__date'].day}.{group['date__date'].month}.{group['date__date'].year}" for group in groups]
    session_amount = [group['cnt'] for group in groups]

    # counting sessions by movie
    movies_and_sessions = Movie.objects.prefetch_related('session_set').all()
    movie_names = [movie.name for movie in movies_and_sessions]
    movie_sessions = [movie.session_set.count() for movie in movies_and_sessions]

    # amount users by city
    city_groups = SimpleUser.objects.all().values('city').annotate(cnt=Count('city')).order_by('city')
    city_names = [group['city'] for group in city_groups]
    city_amount = [group['cnt'] for group in city_groups]

    context = {
        'title': 'KinoCMS | Статистика',
        'males': males,
        'females': females,
        'session_dates': session_dates,
        'session_amount': session_amount,
        'movie_names': movie_names,
        'movie_sessions': movie_sessions,
        'city_names': city_names,
        'city_amount': city_amount,
        'language_blocked': True
    }
    return render(request, 'admin_cms/charts.html', context)


def create_banner(request):
    main_banner_first_record = MainTopBanner.objects.first()
    background_banner_first_record = BackgroundBanner.objects.first()
    news_banner_first_record = NewsBanner.objects.first()

    main_top_banner_form = main_top_banner_form_factory(instance=main_banner_first_record)
    main_top_photo_formset = main_top_formset_factory(
        queryset=main_banner_first_record.maintopbannerphoto_set.all() if main_banner_first_record
        else MainTopBannerPhoto.objects.none())
    background_banner_form = background_banner_form_factory(instance=background_banner_first_record)
    news_banner_form = news_banner_form_factory(instance=news_banner_first_record)
    news_banner_formset = news_banner_formset_factory(
        queryset=news_banner_first_record.newsbannerphoto_set.all() if news_banner_first_record
        else NewsBannerPhoto.objects.none(),
        prefix='news')

    context = {
        'main_top_banner_form': main_top_banner_form,
        'main_top_photo_formset': main_top_photo_formset,
        'background_banner_form': background_banner_form,
        'news_banner_form': news_banner_form,
        'news_banner_formset': news_banner_formset,
        'title': 'KinoCMS | Створення банерів',
        'language_blocked': True
    }

    if request.method == 'POST':

        if 'main_top_banner' in request.POST:
            main_top_banner_form_class = main_top_banner_form_factory(request.POST,
                                                                      request.FILES or None,
                                                                      instance=main_banner_first_record)
            main_top_photo_formset_class = main_top_formset_factory(request.POST,
                                                                    request.FILES or None,
                                                                    queryset=main_banner_first_record.maintopbannerphoto_set.all()
                                                                    if main_banner_first_record
                                                                    else MainTopBannerPhoto.objects.none()
                                                                    )

            if main_top_banner_form_class.is_valid() and main_top_photo_formset_class.is_valid() and \
                    all([form.is_valid() for form in main_top_photo_formset_class]):

                main_banner_saved = main_top_banner_form_class.save()

                for form in main_top_photo_formset_class:
                    if (form.cleaned_data.get('photo') is not None) and (form.cleaned_data.get('url') is not None) \
                            and (form.cleaned_data.get('text') is not None):
                        main_banner_photo_saved = form.save(commit=False)
                        main_banner_photo_saved.main_top_banner = main_banner_saved
                        main_banner_photo_saved.save()

                for deleted_obj in main_top_photo_formset_class.deleted_forms:
                    if deleted_obj.instance.pk:
                        deleted_obj.instance.delete()

                return redirect('create_banner')

            context['main_top_banner_form'] = main_top_banner_form_class
            context['main_top_photo_formset'] = main_top_photo_formset_class

        if 'background_banner' in request.POST:
            background_banner_form_class = background_banner_form_factory(request.POST,
                                                                          request.FILES or None,
                                                                          instance=background_banner_first_record)
            if background_banner_form_class.is_valid():
                background_banner_form_class.save()
                return redirect('create_banner')

            context['background_banner_form'] = background_banner_form_class

        if 'news_banner' in request.POST:
            news_banner_form_class = news_banner_form_factory(request.POST, instance=news_banner_first_record)
            news_banner_formset_class = news_banner_formset_factory(request.POST,
                                                                    request.FILES or None,
                                                                    queryset=news_banner_first_record.newsbannerphoto_set.all()
                                                                    if news_banner_first_record else NewsBannerPhoto.objects.none(),
                                                                    prefix='news')

            if news_banner_form_class.is_valid() and news_banner_formset_class.is_valid() \
                    and all([form.is_valid() for form in news_banner_formset_class]):

                news_banner_saved = news_banner_form_class.save()

                for form in news_banner_formset_class:
                    if form.cleaned_data.get('photo') and form.cleaned_data.get('url'):
                        news_banner_photo_saved = form.save(commit=False)
                        news_banner_photo_saved.news_banner = news_banner_saved
                        news_banner_photo_saved.save()

                for deleted_form in news_banner_formset_class.deleted_forms:
                    if deleted_form.instance.pk:
                        deleted_form.instance.delete()

                return redirect('create_banner')

            context['news_banner_form'] = news_banner_form_class
            context['news_banner_formset'] = news_banner_formset_class

    return render(request, 'admin_cms/banner_form.html', context=context)


def cinema_view(request):
    cinema_list = Cinema.objects.all()

    context = {
        'title': 'KinoCMS| Список кінотеатрів',
        'cinema_list': cinema_list,
        'language_blocked': True
    }
    return render(request, 'admin_cms/cinema.html', context=context)


def create_cinema(request):
    cinema_form = CinemaForm()
    photo_formset = photo_formset_factory(queryset=Photo.objects.none())
    seo_form = seo_form_factory()

    context = {
        'title': 'KinoCMS| Список кінотеатрів',
        'cinema_form': cinema_form,
        'photo_formset': photo_formset,
        'seo_form': seo_form,
    }

    if request.method == 'POST':
        photo_formset_class = photo_formset_factory(request.POST, request.FILES)
        cinema_form_class = CinemaForm(request.POST, request.FILES)
        seo_form_class = seo_form_factory(request.POST)

        if cinema_form_class.is_valid() and seo_form_class.is_valid() \
                and all([form.is_valid() for form in photo_formset_class]):

            # creating new Gallery object manually for usage in cinema_form_class
            new_gallery_object = Gallery.objects.create(name=request.POST['name'])
            new_gallery_object.save()
            new_seo_object = seo_form_class.save()

            # setting for Gallery and SEO field in Cinema gallery and seo created objects
            cinema = cinema_form_class.save(commit=False)
            cinema.gallery = new_gallery_object
            cinema.seo = new_seo_object

            # setting gallery object in gallery field for every photo_form_class
            for photo_form_class in photo_formset_class:
                photo = photo_form_class.save(commit=False)
                photo.gallery = new_gallery_object

            photo_formset_class.save()

            cinema.save()
            return redirect('cinema')

        context['cinema_form'] = cinema_form_class
        context['photo_formset'] = photo_formset_class
        context['seo_form'] = seo_form_class

    return render(request, 'admin_cms/cinema_form.html', context=context)


def update_cinema(request, pk):
    cinema = Cinema.objects.select_related('gallery', 'seo') \
        .prefetch_related('hall_set', 'gallery__photo_set').get(pk=pk)

    cinema_form = CinemaForm(instance=cinema)
    hall_formset = hall_formset_factory(queryset=cinema.hall_set.all(), prefix='hall')
    seo_form = seo_form_factory(instance=cinema.seo)
    photo_formset = photo_formset_factory(queryset=cinema.gallery.photo_set.all())

    context = {
        'cinema_form': cinema_form,
        'hall_formset': hall_formset,
        'photo_formset': photo_formset,
        'seo_form': seo_form,
    }

    if request.method == 'POST':
        photo_formset_class = photo_formset_factory(request.POST, request.FILES,
                                                    queryset=cinema.gallery.photo_set.all())
        cinema_form_class = CinemaForm(request.POST, request.FILES, instance=cinema)
        seo_form_class = seo_form_factory(request.POST, instance=cinema.seo)
        hall_formset_class = hall_formset_factory(request.POST, queryset=cinema.hall_set.all(), prefix='hall')

        if cinema_form_class.is_valid() and seo_form_class.is_valid() and photo_formset_class.is_valid() \
                and hall_formset_class.is_valid() \
                and all([form.is_valid() for form in photo_formset_class]) \
                and all([deleted_form.is_valid() for deleted_form in hall_formset_class.deleted_forms]):

            for form in photo_formset_class:
                form_saved = form.save(commit=False)
                if form_saved.photo:
                    form_saved.gallery = cinema.gallery
                    form_saved.save()

            for deleted_form in hall_formset_class.deleted_forms:
                deleted_form_saved = deleted_form.save(commit=False)
                deleted_form_saved.gallery.delete()
                deleted_form_saved.seo.delete()

            cinema_form_class.save()
            photo_formset_class.save()
            seo_form_class.save()
            hall_formset_class.save()

            return redirect('cinema')

        context['cinema_form'] = cinema_form_class
        context['photo_formset'] = photo_formset_class
        context['seo_form'] = seo_form_class

    return render(request, 'admin_cms/cinema_change_form.html', context=context)


def delete_cinema(request, pk):
    try:
        cinema_to_delete = Cinema.objects.select_related('seo', 'gallery') \
            .prefetch_related('hall_set', 'hall_set__seo', 'hall_set__gallery').get(pk=pk)

        # deleting all related objects to Cinema
        for hall in cinema_to_delete.hall_set.all():
            hall.seo.delete()
            hall.gallery.delete()
            hall.delete()

        cinema_to_delete.gallery.delete()
        cinema_to_delete.seo.delete()
        cinema_to_delete.delete()

    finally:
        return redirect('cinema')


def create_hall(request, cinema_pk):
    hall_form = HallForm()
    photo_formset = photo_formset_factory(queryset=Photo.objects.none())
    seo_form = seo_form_factory()

    if request.method == 'POST':
        hall_form = HallForm(request.POST, request.FILES or None)
        photo_formset = photo_formset_factory(request.POST, request.FILES or None)
        seo_form = seo_form_factory(request.POST)

        if hall_form.is_valid() and photo_formset.is_valid() and all([form.is_valid() for form in photo_formset]) \
                and seo_form.is_valid():

            gallery = Gallery.objects.create(name=f"Hall {request.POST['number']}")
            gallery.save()
            seo_object = seo_form.save()

            for form in photo_formset:
                photo = form.save(commit=False)
                photo.gallery = gallery

            hall_form_saved = hall_form.save(commit=False)
            hall_form_saved.gallery = gallery
            hall_form_saved.cinema_id = Cinema.objects.get(pk=cinema_pk)
            hall_form_saved.seo = seo_object
            hall_form_saved.save()
            photo_formset.save()

            return redirect('update_cinema', pk=cinema_pk)

    context = {
        'title': 'KinoCMS | Створення зала',
        'hall_form': hall_form,
        'photo_formset': photo_formset,
        'seo_form': seo_form,
        'cinema_id': cinema_pk
    }

    return render(request, 'admin_cms/hall_form.html', context=context)


def update_hall(request, hall_pk):
    hall = Hall.objects.select_related('seo', 'gallery').prefetch_related('gallery__photo_set').get(pk=hall_pk)
    hall_form = HallForm(instance=hall)
    seo_form = seo_form_factory(instance=hall.seo)
    photo_formset = photo_formset_factory(queryset=hall.gallery.photo_set.all())

    context = {
        'hall_form': hall_form,
        'seo_form': seo_form,
        'photo_formset': photo_formset,
        'title': 'KinoCMS | Редагування залу'
    }

    if request.method == "POST":
        hall_form = HallForm(request.POST, request.FILES, instance=hall)
        seo_form = seo_form_factory(request.POST, instance=hall.seo)
        photo_formset = photo_formset_factory(request.POST, request.FILES, queryset=hall.gallery.photo_set.all())

        if hall_form.is_valid() and seo_form.is_valid() and photo_formset.is_valid() \
                and all([form.is_valid() for form in photo_formset]):

            hall_saved = hall_form.save()
            seo_form.save()

            gallery_to_save = Gallery.objects.get(pk=hall.gallery.pk)
            gallery_to_save.name = f"Hall {hall_saved.number}"
            gallery_to_save.save()

            for form in photo_formset:
                photo = form.save(commit=False)
                if photo.photo:
                    photo.gallery = hall.gallery
                    photo.save()
            photo_formset.save()

            return redirect('update_cinema', pk=hall.cinema_id.pk)

        context['hall_form'] = hall_form
        context['seo_form'] = seo_form
        context['photo_formset'] = photo_formset

    return render(request, 'admin_cms/hall_change_form.html', context=context)


def movie_view(request):
    movies = Movie.objects.all()

    context = {
        'movies': movies,
        'title': 'KinoCMS | Фільми',
        'language_blocked': True
    }

    return render(request, 'admin_cms/movies.html', context=context)


def create_movie(request):
    movie_form = MovieForm()
    photo_formset = photo_formset_factory(queryset=Photo.objects.none())
    seo_form = seo_form_factory()

    context = {
        'title': 'KinoCMS | Створення фільму',
        'movie_form': movie_form,
        'photo_formset': photo_formset,
        'seo_form': seo_form,
    }

    if request.method == 'POST':
        movie_form_class = MovieForm(request.POST, request.FILES or None)
        photo_formset_class = photo_formset_factory(request.POST, request.FILES or None)
        seo_form_class = seo_form_factory(request.POST)

        if movie_form_class.is_valid() and all([form.is_valid() for form in photo_formset_class]) \
                and seo_form_class.is_valid():
            new_gallery = Gallery.objects.create(name=movie_form_class.cleaned_data.get('name'))
            new_seo = seo_form_class.save()
            movie_url = movie_form_class.cleaned_data.get('trailer_url')
            movie_url = movie_url.replace('watch?v=', 'embed/') + '?autoplay=1&mute=1'
            movie_saved = movie_form_class.save(commit=False)
            movie_saved.gallery = new_gallery
            movie_saved.seo = new_seo
            movie_saved.trailer_url = movie_url
            movie_saved.save()

            for photo in photo_formset_class:
                if photo.cleaned_data.get('photo'):
                    photo_saved = photo.save(commit=False)
                    photo_saved.gallery = new_gallery
                    photo_saved.save()

            return redirect('cinema')

        context['movie_form'] = movie_form_class
        context['photo_formset'] = photo_formset_class
        context['seo_form'] = seo_form_class

    return render(request, 'admin_cms/movie_form.html', context=context)


def update_movie(request, pk):
    movie = Movie.objects.select_related('gallery', 'seo').prefetch_related('gallery__photo_set').get(pk=pk)
    movie_form = MovieForm(instance=movie)
    seo_form = seo_form_factory(instance=movie.seo)
    photo_formset = photo_formset_factory(queryset=movie.gallery.photo_set.all())
    context = {
        'movie_form': movie_form,
        'photo_formset': photo_formset,
        'seo_form': seo_form,
        'title': 'KinoCMS | Оновлення фільму'
    }

    if request.method == 'POST':
        movie_form_class = MovieForm(request.POST, request.FILES, instance=movie)
        seo_form_class = seo_form_factory(request.POST, instance=movie.seo)
        photo_formset_class = photo_formset_factory(request.POST, request.FILES, queryset=movie.gallery.photo_set.all())

        if movie_form_class.is_valid() and seo_form_class.is_valid() and photo_formset_class.is_valid() \
                and all([form.is_valid() for form in photo_formset_class]) \
                and all([deleted_form.is_valid() for deleted_form in photo_formset_class.deleted_forms]):

            for form in photo_formset_class:
                form_saved = form.save(commit=False)
                if form_saved.photo:
                    form_saved.gallery = movie.gallery
                    form.save()

            photo_formset_class.save()
            seo_form_class.save()
            movie_form_class.save()
            return redirect('movie')

        context['movie_form'] = movie_form_class
        context['seo_form'] = seo_form_class
        context['photo_formset'] = photo_formset_class

    return render(request, 'admin_cms/movie_change_form.html', context=context)


# separate creator for news
def news_create(request):
    news_form = EventForm()
    photo_formset = photo_formset_factory(queryset=Photo.objects.none())
    seo_form = seo_form_factory()

    context = {
        'title': 'KinoCMS | Створення новини',
        'news_form': news_form,
        'photo_formset': photo_formset,
        'seo_form': seo_form
    }

    if request.method == 'POST':
        news_form_class = EventForm(request.POST, request.FILES or None)
        photo_formset_class = photo_formset_factory(request.POST, request.FILES or None)
        seo_form_class = seo_form_factory(request.POST)

        if news_form_class.is_valid() and all([form.is_valid() for form in photo_formset_class]) \
                and seo_form_class.is_valid():
            new_gallery = Gallery.objects.create(name=news_form_class.cleaned_data.get('name'))
            new_seo = seo_form_class.save()
            news_saved = news_form_class.save(commit=False)
            news_saved.gallery = new_gallery
            news_saved.type = 'news'
            news_saved.seo = new_seo
            news_saved.save()

            for photo in photo_formset_class:
                if photo.cleaned_data.get('photo'):
                    photo_saved = photo.save(commit=False)
                    photo_saved.gallery = new_gallery
                    photo_saved.save()

            return redirect('news')

        context['news_form'] = news_form_class
        context['photo_formset'] = photo_formset_class
        context['seo_form'] = seo_form_class

    return render(request, 'admin_cms/news_form.html', context=context)


# separate viewer for news
def news_view(request):
    news = Event.objects.filter(type='news')

    context = {
        'news_list': news,
        'title': 'KinoCMS | Новини',
        'language_blocked': True
    }

    return render(request, 'admin_cms/news.html', context=context)


# separate creator for events
def event_create(request):
    event_form = EventForm()
    photo_formset = photo_formset_factory(queryset=Photo.objects.none())
    seo_form = seo_form_factory()

    context = {
        'title': 'KinoCMS | Створення події',
        'event_form': event_form,
        'photo_formset': photo_formset,
        'seo_form': seo_form
    }

    if request.method == 'POST':
        event_form_class = EventForm(request.POST, request.FILES or None)
        photo_formset_class = photo_formset_factory(request.POST, request.FILES or None)
        seo_form_class = seo_form_factory(request.POST)

        if event_form_class.is_valid() and all([form.is_valid() for form in photo_formset_class]) \
                and seo_form_class.is_valid():
            new_gallery = Gallery.objects.create(name=event_form_class.cleaned_data.get('name'))
            new_seo = seo_form_class.save()
            event_saved = event_form_class.save(commit=False)
            event_saved.gallery = new_gallery
            event_saved.type = 'event'
            event_saved.seo = new_seo
            event_saved.save()

            for photo in photo_formset_class:
                if photo.cleaned_data.get('photo'):
                    photo_saved = photo.save(commit=False)
                    photo_saved.gallery = new_gallery
                    photo_saved.save()

            return redirect('events')

        context['event_form'] = event_form_class
        context['photo_formset'] = photo_formset_class
        context['seo_form'] = seo_form_class

    return render(request, 'admin_cms/event_form.html', context=context)


# separate viewer for events
def event_view(request):
    events = Event.objects.filter(type='event')

    context = {
        'events': events,
        'title': 'KinoCMS | Події',
        'language_blocked': True
    }

    return render(request, 'admin_cms/events.html', context=context)


# common editor for news and events
def update_event(request, pk):
    event_record = Event.objects.select_related('seo').prefetch_related('gallery__photo_set').get(pk=pk)
    event_form = EventForm(instance=event_record)
    photo_formset = photo_formset_factory(queryset=event_record.gallery.photo_set.all())
    seo_form = seo_form_factory(instance=event_record.seo)

    context = {
        'title': 'KinoCMS | Створення події',
        'event_form': event_form,
        'photo_formset': photo_formset,
        'seo_form': seo_form
    }

    if request.method == 'POST':
        event_form_class = EventForm(request.POST, request.FILES, instance=event_record)
        seo_form_class = seo_form_factory(request.POST, instance=event_record.seo)
        photo_formset_class = photo_formset_factory(request.POST, request.FILES, queryset=event_record.gallery.photo_set.all())

        if event_form_class.is_valid() and seo_form_class.is_valid() and photo_formset_class.is_valid() \
                and all([form.is_valid() for form in photo_formset_class]) \
                and all([deleted_form.is_valid() for deleted_form in photo_formset_class.deleted_forms]):

            for form in photo_formset_class:
                form_saved = form.save(commit=False)
                if form_saved.photo:
                    form_saved.gallery = event_record.gallery
                    form.save()

            photo_formset_class.save()
            seo_form_class.save()
            event_form_class.save()
            return redirect('events')

        context['event_form'] = event_form_class
        context['seo_form'] = seo_form_class
        context['photo_formset'] = photo_formset_class

    return render(request, 'admin_cms/event_change_form.html', context=context)


# common deleter for news and events
def delete_event(request, pk):
    event_to_delete = Event.objects.get(pk=pk)
    event_to_delete.gallery.delete()
    event_to_delete.seo.delete()
    event_to_delete.delete()

    return redirect('events')


def main_page_create_update(request):
    main_page_record = MainPage.objects.select_related('seo').first()
    main_page = main_page_form_factory(instance=main_page_record)
    seo_form = seo_form_factory(instance=main_page_record.seo if main_page_record else None)

    context = {
        'main_page': main_page,
        'seo_form': seo_form,
        'title': 'KinoCMS | Створення головної сторінки',
        'language_blocked': True
    }
    if request.method == 'POST':
        main_page = main_page_form_factory(request.POST, instance=main_page_record)
        seo_form = seo_form_factory(request.POST, instance=main_page_record.seo if main_page_record else None)

        if main_page.is_valid() and seo_form.is_valid():
            seo_form_saved = seo_form.save()
            main_page_saved = main_page.save(commit=False)
            if not main_page_record:
                main_page_saved.seo = seo_form_saved
            main_page_saved.save()

            return redirect('pages')

        context['main_page'] = main_page
        context['seo_form'] = seo_form

    return render(request, 'admin_cms/main_page_change_form.html', context=context)


def contact_page_create(request):
    contact_records = Contacts.objects.all().order_by('pk')
    contact_formset = (func_contact_formset_factory(0 if contact_records else 1))(queryset=contact_records)

    context = {
        'have_records': True if contact_records else False,
        'contact_formset': contact_formset,
        'language_blocked': True
    }

    if request.method == 'POST':
        contact_formset_class = (func_contact_formset_factory(0 if contact_records else 1))(request.POST,
                                                                                            request.FILES,
                                                                                            queryset=contact_records)

        if contact_formset_class.is_valid():
            contact_formset_class.save()
            return redirect('pages')

        context['contact_formset'] = contact_formset_class

    return render(request, 'admin_cms/contact_form.html', context=context)


def page_view(request):
    main_page = MainPage.objects.first()
    about_cinema = Page.objects.get(type='about_cinema')
    cafe_bar = Page.objects.get(type='cafe_bar')
    vip_hall = Page.objects.get(type='vip_hall')
    advertisment = Page.objects.get(type='advertisment')
    baby_room = Page.objects.get(type='baby_room')
    pages = Page.objects.filter(type=None)

    context = {
        'main_page': main_page,
        'about_cinema': about_cinema,
        'cafe_bar': cafe_bar,
        'vip_hall': vip_hall,
        'advertisment': advertisment,
        'baby_room': baby_room,
        'pages': pages,
        'title': 'KinoCMS | Сторінки',
        'language_blocked': True
    }

    return render(request, 'admin_cms/pages.html', context=context)


def create_page(request):
    page_form = PageCreateForm()
    seo_form = seo_form_factory()
    photo_formset = photo_formset_factory(queryset=Photo.objects.none())

    context = {
        'page_form': page_form,
        'seo_form': seo_form,
        'photo_formset': photo_formset,
        'title': 'KinoCMS | Створення сторінок'
    }

    if request.method == 'POST':
        page_form_class = PageCreateForm(request.POST, request.FILES)
        photo_formset_class = photo_formset_factory(request.POST, request.FILES)
        seo_form_class = seo_form_factory(request.POST)

        if page_form_class.is_valid() and photo_formset_class.is_valid() and photo_formset_class.is_valid() \
                and all([form.is_valid() for form in photo_formset_class]) and seo_form_class.is_valid():

            new_gallery = Gallery.objects.create(name=page_form_class.cleaned_data.get('name'))
            seo_saved = seo_form_class.save()
            page_saved = page_form_class.save(commit=False)
            page_saved.gallery = new_gallery
            page_saved.seo = seo_saved
            page_saved.save()

            for form in photo_formset_class:
                if form.cleaned_data.get('photo'):
                    form_saved = form.save(commit=False)
                    form_saved.gallery = new_gallery
                    form_saved.save()

            return redirect('pages')

        context['page_form'] = page_form_class
        context['seo_form'] = seo_form_class
        context['photo_formset'] = photo_formset_class

    return render(request, 'admin_cms/page_form.html', context=context)


def update_page(request, pk):
    page = Page.objects.select_related('gallery', 'seo').prefetch_related('gallery__photo_set').get(pk=pk)

    page_form = PageCreateForm(instance=page)
    photo_formset = photo_formset_factory(queryset=page.gallery.photo_set.all())
    seo_form = seo_form_factory(instance=page.seo)

    context = {
        'title': 'KinoCMS | Оновлення сторінки',
        'page_form': page_form,
        'photo_formset': photo_formset,
        'seo_form': seo_form
    }

    if request.method == 'POST':
        photo_formset_class = photo_formset_factory(request.POST, request.FILES,
                                                    queryset=page.gallery.photo_set.all())
        page_form_class = PageCreateForm(request.POST, request.FILES, instance=page)
        seo_form_class = seo_form_factory(request.POST, instance=page.seo)

        if page_form_class.is_valid() and seo_form_class.is_valid() and photo_formset_class.is_valid() \
                and all([form.is_valid() for form in photo_formset_class]):

            for form in photo_formset_class:
                form_saved = form.save(commit=False)
                if form_saved.photo:
                    form_saved.gallery = page.gallery
                    form_saved.save()

            page_form_class.save()
            photo_formset_class.save()
            seo_form_class.save()

            return redirect('pages')

        context['page_form'] = page_form_class
        context['photo_formset'] = photo_formset_class
        context['seo_form'] = seo_form_class

    return render(request, 'admin_cms/page_change_form.html', context=context)


def delete_page(request, pk):
    try:
        page = Page.objects.get(pk=pk)

        if page.type:
            return HttpResponseForbidden()

        page.gallery.delete()
        page.seo.delete()
        page.delete()

    finally:
        return redirect('pages')


def users(request):
    simple_users = SimpleUser.objects.all()

    context = {
        'title': 'KinoCMS | Користувачі',
        'users': simple_users,
        'language_blocked': True
    }
    return render(request, 'admin_cms/users.html', context=context)


def user_update(request, pk):
    if request.user.is_superuser:
        try:
            simple_user_instance = SimpleUser.objects.get(pk=pk)
            simple_user = UserFormUpdate(instance=simple_user_instance)
            context = {
                'simple_user': simple_user,
                'title': 'KinoCMS | Редагування користувача',
                'language_blocked': True
            }
            if request.method == 'POST':
                simple_user_class = UserFormUpdate(request.POST, instance=simple_user_instance)
                if simple_user_class.is_valid():

                    # saving old password for occasion if new password not entered
                    old_password = SimpleUser.objects.get(pk=pk).password

                    new_password = simple_user_class.cleaned_data.get('password')
                    user_saved = simple_user_class.save()
                    if new_password:
                        user = SimpleUser.objects.get(email=user_saved.email)
                        user.set_password(new_password)
                        user.save()

                    # if no password were entered, old password is set again
                    else:
                        user_saved.password = old_password
                        user_saved.save()
                    return redirect('users')
                context = {
                    'simple_user': simple_user_class,
                    'title': 'KinoCMS | Редагування користувача',
                    'language_blocked': True
                }
                return render(request, 'admin_cms/user_change_form.html', context=context)

            return render(request, 'admin_cms/user_change_form.html', context=context)

        except:
            return redirect('users')

    return HttpResponseForbidden()


def user_delete(request, pk):
    if request.user.is_superuser:
        try:
            user_to_delete = SimpleUser.objects.get(pk=pk)
            user_to_delete.delete()
        finally:
            return redirect('users')
    return HttpResponseForbidden()


def send_email_view(request):
    simple_users = SimpleUser.objects.all()
    user_data_form = SendMail()
    files = MailFile.objects.all().order_by('-created_at')[:5]

    context = {
        'title': 'KinoCMS | Розсилка',
        'simple_users': simple_users,
        'user_data_form': user_data_form,
        'language_blocked': True,
        'files': files,
    }

    if request.method == 'POST':
        user_data_form_class = SendMail(request.POST, request.FILES)

        if user_data_form_class.is_valid():

            file = MailFile.objects.get(pk=int(request.POST['file-for-mailing']))
            text_to_send = file.file.open('r').read()

            if user_data_form_class.cleaned_data.get('all_users') == 'True':
                sending_mail.delay('Розсилка з KinoCMS',
                                   text_to_send,
                                   settings.EMAIL_HOST_USER,
                                   [simple_user.email for simple_user in SimpleUser.objects.all()])

            elif user_data_form_class.cleaned_data.get('all_users') == 'False':
                user_list = user_data_form_class.data.getlist('send_to_current_user')
                sending_mail.delay('Розсилка із KinoCMS', text_to_send, settings.EMAIL_HOST_USER, user_list)

            return redirect('cinema')

    return render(request, 'admin_cms/mailing.html', context)


def files(request):
    if request.method == 'POST':
        try:
            file_to_save = request.FILES['file']
            MailFile.objects.create(file=file_to_save)
        finally:
            mailing_files = MailFile.objects.all().order_by('-created_at')
            if len(mailing_files) > 5:
                mailing_files = mailing_files[:5]
                mailing_files_difference = [record for record in mailing_files if record not in mailing_files[:5]]
                for record in mailing_files_difference:
                    record.delete()

            context = {
                'files': [(file.id, file.filename()) for file in mailing_files]
            }

            return JsonResponse(context)

