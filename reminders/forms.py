from django import forms
from .models import HabitReminder

class ReminderTimeForm(forms.ModelForm):
    class Meta:
        model = HabitReminder
        fields = ['reminder_time']
        widgets = {
            'reminder_time': forms.TimeInput(attrs={'type': 'time'})
        }
