import json

from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from cinema.views import header_data
from .models import *
from user.models import Ticket


def movie_detail(request, movie_pk):

    movie = Movie.objects.prefetch_related('gallery__photo_set', 'session_set').get(pk=movie_pk)

    if request.is_ajax():
        if request.GET['type'] != 'all':
            type_movie = request.GET['type']
            sessions = Session.objects.prefetch_related('hall').filter(movie=movie, type=type_movie)
        else:
            sessions = Session.objects.prefetch_related('hall').filter(movie=movie)
        sessions_json = json.loads(serialize('json', sessions))
        halls_json = json.loads(serialize('json', Hall.objects.filter(session__movie=movie)))
        return JsonResponse({'sessions': sessions_json, 'halls': halls_json})

    sessions = Session.objects.filter(movie=movie)

    context = {
        'title': f'KinoCMS | Фільм "{movie.name}"',
        'sessions': sessions,
        'movie': movie,
    }
    context.update(header_data(request))

    return render(request, 'movie/movie_detail.html', context)


def schedule_view(request):

    if request.is_ajax():

        types = request.GET.getlist('types[]')
        cinema = request.GET.get('cinema')
        movie = request.GET.get('movie')
        date = request.GET.getlist('date[]')
        hall = request.GET.get('hall')

        filters_types = Q()
        filters_cinema = Q()
        filters_movie = Q()
        filters_date = Q()
        filters_hall = Q()

        if types:
            filters_types = Q(type=types[0])
            if len(types) > 1:
                filters_types = Q(type=types[0]) | Q(type=types[1])

        if cinema:
            filters_cinema = Q(hall__cinema_id__name_uk=cinema) | Q(hall__cinema_id__name_ru=cinema)
        if movie:
            filters_movie = Q(movie__name_uk=movie) | Q(movie__name_ru=movie)
        if date:
            if len(date) > 1:
                searching_date = timezone.datetime(int(date[2]), int(date[1]), int(date[0]))
                filters_date = Q(date__date=searching_date)
        if hall:
            filters_hall = Q(hall__number=int(hall))
        sessions = Session.objects.select_related('movie', 'hall', 'hall__cinema_id').filter(filters_types &
                                                                          filters_cinema &
                                                                          filters_movie &
                                                                          filters_date &
                                                                          filters_hall).order_by('date')
        dates = []
        for session in sessions:
            # add date, which date.date() not in dates[] yet
            dates.append(session.date) if all(
                [date_time.date() != session.date.date() for date_time in dates]) else None
        session_json = json.loads(serialize('json', sessions))

        for index, session in enumerate(session_json):
            session['fields']['movie'] = sessions[index].movie.name
            session['fields']['hall'] = sessions[index].hall.number
            session['fields']['price'] = int(session['fields']['price'])

        return JsonResponse({'sessions': session_json, 'dates': dates})

    sessions = Session.objects.select_related('movie', 'hall', 'hall__cinema_id').all().order_by('date')

    # lists for further selecting and sorting in template
    dates = []
    for session in sessions:
        # add date, which date.date() not in dates[] yet
        dates.append(session.date) if all([date_time.date() != session.date.date() for date_time in dates]) else None
    cinemas = set([session.hall.cinema_id for session in sessions])
    movies = []
    for session in sessions:
        # add date, which date.date() not in dates[] yet
        movies.append(session.movie) if all([movie.name != session.movie.name for movie in movies]) else None
    halls = set([session.hall for session in sessions])

    context = {
        'title': 'KinoCMS | Розклад',
        'sessions': sessions,
        'dates': dates,
        'cinema': cinemas,
        'movies': movies,
        'halls': halls
    }
    context.update(header_data(request))

    return render(request, 'movie/schedule.html', context)


def book_tickets_view(request, session_pk):
    session = Session.objects.select_related('movie', 'hall').prefetch_related('ticket_set', 'ticket_set__user')\
        .get(pk=session_pk)

    context = {
        'title': 'KinoCMS | Бронювання та купівля квитків',
        'session': session,
        'rows': [number for number in range(1, session.hall.row_amount + 1)],
        'seats': [number for number in range(1, session.hall.seat_amount + 1)],
        'booked_seats': [f'{ticket.row_number} {ticket.seat_number}' for ticket in session.ticket_set.all()],
    }
    context.update(header_data(request))

    if request.method == 'POST':
        seat_list = (request.POST['seat_list']).split(';')[:-1]     # last element always is - ''

        for seat_string in seat_list:
            Ticket.objects.create(session=session,
                                  user=request.user,
                                  row_number=int(seat_string[0]),
                                  seat_number=int(seat_string[2]))
        return redirect('home')

    return render(request, 'movie/book_ticket.html', context)
