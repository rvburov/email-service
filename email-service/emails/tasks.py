# -*- coding: utf-8 -*-
import logging
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import Mailing, Subscriber, MailingLog
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse

logger = logging.getLogger(__name__)

@shared_task
def send_mailing(mailing_id):
    logger.info("Запущена задача send_mailing для рассылки с ID: {} (время по Москве: {})".format(mailing_id, timezone.localtime(timezone.now())))
    try:
        mailing = Mailing.objects.get(id=mailing_id)
        subscribers = Subscriber.objects.all()

        if not subscribers.exists():
            logger.info("Список подписчиков пустой")
            return

        for subscriber in subscribers:
            # Заменяем переменные в шаблоне
            try:
                html_content = mailing.template.replace("{{ first_name }}", subscriber.first_name)
                html_content = html_content.replace("{{ last_name }}", subscriber.last_name)
                html_content = html_content.replace("{{ birthday }}", str(subscriber.birthday))
                html_content = html_content.replace("{{ mailing.id }}", str(mailing.id))  # Заменяем переменную mailing.id
                html_content = html_content.replace("{{ subscriber.id }}", str(subscriber.id))  # Заменяем переменную subscriber.id
            except KeyError as e:
                logger.error("Переменная не найдена в шаблоне: {}".format(e))
                return JsonResponse({'error': 'Переменная не найдена в шаблоне'}, status=400)

            # Отправка письма
            msg = EmailMultiAlternatives(
                mailing.subject,
                html_content,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # Создаем лог для каждого подписчика
            log, created = MailingLog.objects.get_or_create(mailing=mailing, subscriber=subscriber)
            if created:
                logger.info("Создан новый лог: mailing_id={}, subscriber_id={}".format(mailing.id, subscriber.id))
            else:
                logger.info("Лог уже существует: mailing_id={}, subscriber_id={}".format(mailing.id, subscriber.id))

        # Обновление статуса рассылки
        mailing.is_sent = True
        mailing.save()
        logger.info("Статус рассылки с ID: {} обновлен на 'Отправлено'".format(mailing_id))
        
        logger.info("Задача send_mailing для рассылки с ID: {} выполнена успешно (время по Москве: {})".format(mailing_id, timezone.localtime(timezone.now())))
    except Exception as e:
        logger.error("Ошибка при выполнении задачи send_mailing для рассылки с ID: {}: {}".format(mailing_id, e))
        raise e