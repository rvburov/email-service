# -*- coding: utf-8 -*-
"""Конфигурация административной панели для моделей."""

from django.contrib import admin
from .models import Subscriber, Mailing, MailingLog

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Административная панель для управления подписчиками."""
    
    list_display = ('email', 'first_name', 'last_name', 'birthday')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('birthday',)
    ordering = ('email',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Административная панель для управления рассылками."""
    
    list_display = ('subject', 'scheduled_time', 'is_sent')
    list_filter = ('is_sent', 'scheduled_time')
    search_fields = ('subject',)
    date_hierarchy = 'scheduled_time'
    actions = ['mark_as_sent']

    def mark_as_sent(self, request, queryset):
        queryset.update(is_sent=True)
    mark_as_sent.short_description = "Отметить как отправленное"

@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    """Административная панель для просмотра логов рассылки."""
    
    list_display = ('mailing', 'subscriber', 'opened_at')
    list_filter = ('mailing', 'subscriber', 'opened_at')
    search_fields = ('mailing__subject', 'subscriber__email')
    readonly_fields = ('opened_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('mailing', 'subscriber')
