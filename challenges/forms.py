from django import forms
from .models import Challenge

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'difficulty', 'duration_days', 'start_date', 'contestants']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
