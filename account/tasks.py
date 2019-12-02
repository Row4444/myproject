from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_user(email, token):
    send_mail('Activate',
              "Activate your account. {}".format(token),
              'myproject4089@gmail.com',
              [email])
    return None
