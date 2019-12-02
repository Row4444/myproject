from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_comment(post, email, comment):
    send_mail('New comment for ' + post,
              comment,
              'myproject4089@gmail.com',
              [email],)
    return None
