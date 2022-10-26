from django.shortcuts import render

from cinema.views import header_data
from .models import *


def event_view(request):
    events = Event.objects.filter(type='event', status=True)

    context = {
        'title': 'KinoCMS | Акції',
        'events': events
    }
    context.update(header_data(request))

    return render(request, 'event/event_view.html', context)


def event_detail(request, event_pk):
    event = Event.objects.get(pk=event_pk)

    context = {
        'title': 'KinoCMS | Огляд акції',
        'event': event
    }
    context.update(header_data(request))

    return render(request, 'event/event_detail.html', context)


def news_view(request):
    news = Event.objects.filter(type='news', status=True)

    context = {
        'title': 'KinoCMS | Новини',
        'news_list': news
    }
    context.update(header_data(request))

    return render(request, 'event/news_view.html', context)


def news_detail(request, news_pk):
    news = Event.objects.get(pk=news_pk)

    context = {
        'title': 'KinoCMS | Новина',
        'news': news
    }
    context.update(header_data(request))

    return render(request, 'event/news_detail.html', context)