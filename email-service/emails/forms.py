from django import forms
from .models import EmailCampaign
from django.utils import timezone

class EmailCampaignForm(forms.ModelForm):
    class Meta:
        model = EmailCampaign
        fields = ['subject', 'template', 'send_date']

    def clean_send_date(self):
        send_date = self.cleaned_data['send_date']
        if send_date < timezone.now():
            raise forms.ValidationError("Дата отправки не может быть в прошлом.")
        return send_date
