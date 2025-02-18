# -*- coding: utf-8 -*-
"""Форма для создания и валидации email-рассылки."""

from django import forms
from django.utils import timezone
from .models import Mailing


class EmailCampaignForm(forms.ModelForm):
    """Форма для создания email-кампании."""

    class Meta:
        model = Mailing
        fields = ['subject', 'template', 'scheduled_time']

    def clean_scheduled_time(self):
        """Проверяет, что дата отправки находится в будущем."""
        scheduled_time = self.cleaned_data['scheduled_time']
        if scheduled_time < timezone.now():
            raise forms.ValidationError(
                "Дата отправки не может быть в прошлом."
            )
        return scheduled_time
