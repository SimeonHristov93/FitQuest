from django import forms
from .models import ProgressEntry

class ProgressEntryForm(forms.ModelForm):
    class Meta:
        model = ProgressEntry
        fields = ['day', 'value']
        labels = {
            'day': 'Day',
            'value': 'Reps or Mins',
        }

    def clean_day(self):
        day = self.cleaned_data['day']
        if day < 1:
            raise forms.ValidationError("Day must be positive.")
        return day
