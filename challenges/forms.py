from django import forms
from .models import Challenge

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        exclude = ['creator', 'created_at']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }