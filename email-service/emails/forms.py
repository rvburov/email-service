from django import forms
from .models import EmailCampaign

class EmailCampaignForm(forms.ModelForm):
    class Meta:
        model = EmailCampaign
        fields = ['subject', 'template', 'send_date']
