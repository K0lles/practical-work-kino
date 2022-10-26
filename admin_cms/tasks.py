from __future__ import unicode_literals

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def sending_mail(subject, text, user_host, receivers, *args, **kwargs):
    send_mail(subject, text, user_host, receivers)
    return 'Performed by sendingmail'
