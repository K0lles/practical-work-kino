from django.db.models import Count
from django.shortcuts import render

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
