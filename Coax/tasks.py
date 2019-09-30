from celery import shared_task
from django.core.mail import EmailMultiAlternatives


@shared_task
def notify_admins(message):

    to_list= _get_to_list()
    mail = EmailMultiAlternatives(
        'New lesson added',message, to=to_list
    )
    mail.attach_alternative(message,'text/html')
    mail.send()