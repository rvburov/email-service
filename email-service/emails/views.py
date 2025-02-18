# -*- coding: utf-8 -*-
"""Обработчики представлений для управления email-рассылками и подписчиками."""

import logging
import os
import re
import codecs
from datetime import datetime
from dateutil.parser import parse

import pandas as pd
from io import TextIOWrapper

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Subscriber, Mailing, MailingLog
from .tasks import send_mailing

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def homepage(request):
    """Отображает главную страницу сервиса рассылок."""
    return render(request, 'emails/homepages.html')


@csrf_exempt
def track_email_open(request, mailing_id, subscriber_id):
    """Фиксирует факт открытия письма подписчиком."""
    logger.info(
        "Запрос на отслеживание открытия: mailing_id={}, subscriber_id={}".format(
            mailing_id, subscriber_id
        )
    )
    try:
        mailing_log = MailingLog.objects.get(
            mailing_id=mailing_id, subscriber_id=subscriber_id
        )
        if not mailing_log.opened_at:
            mailing_log.opened_at = timezone.now()
            mailing_log.save()
            logger.info(
                "Статус прочтения обновлен: mailing_id={}, subscriber_id={}".format(
                    mailing_id, subscriber_id
                )
            )
        return HttpResponse(status=200)
    except MailingLog.DoesNotExist:
        logger.error("Лог не найден: mailing_id={}, subscriber_id={}".format(
            mailing_id, subscriber_id
        ))
        return HttpResponse(status=404)


def create_email(request):
    """Создает новую email-рассылку на основе шаблона или пользовательского ввода."""
    if request.method == 'POST':
        subject = request.POST.get('subject')
        template_option = request.POST.get('template_option')

        # Определение шаблона письма
        if template_option == 'custom':
            template = request.POST.get('template')
        else:
            predefined_template = request.POST.get('predefined_template')
            template_path = os.path.join(
                os.path.dirname(__file__), 'templates/mailing', predefined_template
            )
            if not os.path.exists(template_path):
                logger.error("Файл шаблона не найден: {}".format(template_path))
                return JsonResponse({'error': 'Файл шаблона не найден'}, status=404)
            with codecs.open(template_path, 'r', encoding='utf-8') as file:
                template = file.read()

        scheduled_time = request.POST.get('scheduled_time')

        # Валидация даты и времени отправки
        if scheduled_time:
            try:
                scheduled_time_parsed = timezone.make_aware(
                    datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M'),
                    timezone.get_current_timezone()
                )
                if scheduled_time_parsed < timezone.now():
                    return JsonResponse(
                        {'error': 'Дата и время отправки должны быть в будущем'},
                        status=400
                    )
            except ValueError as e:
                logger.error("Ошибка преобразования даты и времени: {}".format(e))
                return JsonResponse(
                    {'error': 'Некорректный формат даты и времени'}, status=400
                )
        else:
            scheduled_time_parsed = timezone.now()

        scheduled_time_msk = scheduled_time_parsed.astimezone(
            timezone.get_current_timezone()
        )

        # Проверка списка подписчиков
        if not Subscriber.objects.exists():
            logger.info("Список подписчиков пустой")
            return JsonResponse({'error': 'Список подписчиков пустой'}, status=400)

        # Создание рассылки
        try:
            mailing = Mailing.objects.create(
                subject=subject, template=template, scheduled_time=scheduled_time_msk
            )
        except Exception as e:
            logger.error("Ошибка при создании рассылки: {}".format(e))
            return JsonResponse({'error': 'Ошибка при создании рассылки'}, status=500)

        # Запуск задачи Celery
        try:
            send_mailing.apply_async(args=[mailing.id], eta=scheduled_time_msk)
        except Exception as e:
            logger.error("Ошибка при запуске задачи Celery: {}".format(e))
            return JsonResponse(
                {'error': 'Ошибка при запуске задачи Celery'}, status=500
            )

        return JsonResponse({'status': 'success'})

    return render(request, 'emails/create_email.html')


def email_list(request):
    """Отображает список всех рассылок."""
    mailings = Mailing.objects.all().prefetch_related('mailinglog_set')
    return render(request, 'emails/email_list.html', {'mailings': mailings})


def subscriber_list(request):
    """Отображает список подписчиков."""
    subscribers = Subscriber.objects.all()
    return render(request, 'emails/subscriber_list.html', {'subscribers': subscribers})


def is_valid_email(email):
    """Проверяет валидность email-адреса с помощью регулярного выражения."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)


def upload_subscribers(request):
    """Загружает подписчиков из CSV-файла."""
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')

        # Определение разделителя
        first_line = csv_file.readline().strip()
        csv_file.seek(0)
        delimiter = ',' if ',' in first_line else ';'

        # Чтение CSV-файла с использованием pandas
        df = pd.read_csv(csv_file, delimiter=delimiter)

        for index, row in df.iterrows():
            try:
                email = unicode(row['email'], 'utf-8')
                first_name = unicode(row['first_name'], 'utf-8')
                last_name = unicode(row['last_name'], 'utf-8')
                birthday = parse(unicode(row['birthday'], 'utf-8')).strftime('%Y-%m-%d')

                if not is_valid_email(email):
                    logger.warning(u"Некорректный email: {}".format(email))
                    continue

                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(
                        email=email, first_name=first_name,
                        last_name=last_name, birthday=birthday
                    )
                else:
                    logger.warning(
                        u"Подписчик с email {} уже существует".format(email)
                    )
            except KeyError as e:
                logger.error(u"Отсутствует ключ: {}".format(e))
            except UnicodeEncodeError as e:
                logger.error(u"Ошибка кодировки: {}".format(e))
            except ValueError as e:
                logger.error(u"Ошибка преобразования даты: {}".format(e))

        return redirect('subscriber_list')

    return redirect('homepage')


def delete_subscriber(request, email):
    """Удаляет подписчика из базы данных."""
    if request.method == 'POST':
        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.delete()
            logger.info(u"Подписчик с email {} был удален".format(email))
            return JsonResponse({'status': 'success'}, status=200)
        except Subscriber.DoesNotExist:
            logger.error(u"Подписчик с email {} не найден".format(email))
            return JsonResponse({'error': 'Subscriber not found'}, status=404)

    logger.error(u"Некорректный запрос")
    return JsonResponse({'error': 'Invalid request'}, status=400)
