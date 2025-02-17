# -*- coding: utf-8 -*-
from django.db import models

class Subscriber(models.Model):
    """Модель подписчика с email, именем, фамилией и датой рождения."""

    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birthday = models.DateField(verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.email)


class Mailing(models.Model):
    """Модель email-рассылки с темой, шаблоном, датой отправки и статусом."""

    subject = models.CharField(max_length=200, verbose_name="Тема")
    template = models.TextField(verbose_name="Шаблон письма")
    scheduled_time = models.DateTimeField(verbose_name="Дата и время отправки")
    is_sent = models.BooleanField(default=False, verbose_name="Отправлено")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return self.subject


class MailingLog(models.Model):
    """Лог открытия письма, связывающий рассылку и подписчика."""

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, verbose_name="Подписчик")
    opened_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата открытия")

    class Meta:
        verbose_name = "Лог рассылки"
        verbose_name_plural = "Логи рассылок"

    def __str__(self):
        return "{} - {}".format(self.mailing.subject, self.subscriber.email)
