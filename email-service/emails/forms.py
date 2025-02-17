# -*- coding: utf-8 -*-
from django import forms
from .models import Mailing
from django.utils import timezone

class EmailCampaignForm(forms.ModelForm):
    """Форма для создания и валидации email-рассылки."""
    class Meta:
        model = Mailing
        fields = ['subject', 'template', 'scheduled_time']

    def clean_scheduled_time(self):
        scheduled_time = self.cleaned_data['scheduled_time']
        if scheduled_time < timezone.now():
            raise forms.ValidationError("Дата отправки не может быть в прошлом.")
        return scheduled_time
