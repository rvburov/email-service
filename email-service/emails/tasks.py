from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import Mailing, Subscriber, MailingLog

@shared_task
def send_mailing(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        html_content = mailing.template.replace("{{ first_name }}", subscriber.first_name)
        html_content = html_content.replace("{{ last_name }}", subscriber.last_name)
        html_content = html_content.replace("{{ birthday }}", str(subscriber.birthday))

        msg = EmailMultiAlternatives(
            mailing.subject,
            html_content,
            'from@example.com',
            [subscriber.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        MailingLog.objects.create(mailing=mailing, subscriber=subscriber)
