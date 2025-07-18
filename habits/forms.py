from django import forms 
from .models import Habit, User 

class HabitForm(forms.ModelForm):
    class Meta: 
        model = Habit
        fields = '__all__'

class UserForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['name', 'email', 'date_of_birth', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)

