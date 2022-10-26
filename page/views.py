from django.shortcuts import render
from django.utils.translation import ugettext as _

from .models import *
from cinema.views import header_data


def advertisment_view(request):
    advertisment = Page.objects.prefetch_related('gallery__photo_set').get(type='advertisment')

    context = {
        'title': 'KinoCMS | Реклама',
        'head': 'Реклама',
        'record': advertisment
    }
    context.update(header_data(request))

    return render(request, 'page/page_render.html', context)


def cafe_bar_detail(request):
    cafe_bar = Page.objects.prefetch_related('gallery__photo_set').get(type='cafe_bar')

    context = {
        'head': 'Кафе-бар',
        'title': 'KinoCMS | Кафе-бар',
        'record': cafe_bar
    }
    context.update(header_data(request))

    return render(request, 'page/page_render.html', context)


def vip_hall_view(request):
    vip_hall = Page.objects.prefetch_related('gallery__photo_set').get(type='vip_hall')

    context = {
        'title': 'KinoCMS | Реклама',
        'head': _('Реклама'),
        'record': vip_hall
    }
    context.update(header_data(request))

    return render(request, 'page/page_render.html', context)


def baby_room_view(request):
    baby_room = Page.objects.prefetch_related('gallery__photo_set').get(type='baby_room')

    context = {
        'title': 'KinoCMS | Реклама',
        'head': _('Дитяча кімната'),
        'record': baby_room
    }
    context.update(header_data(request))

    return render(request, 'page/page_render.html', context)


def contacts_view(request):
    contacts = Contacts.objects.all()

    context = {
        'title': 'KinoCMS | Контакти',
        'contacts': contacts
    }

    return render(request, 'page/contacts_view.html', context)


def mobile_applications(request):
    context = {
        'title': 'KinoCMS | Мобільні додатки'
    }
    context.update(header_data(request))

    return render(request, 'page/mobile_application_view.html', context)
