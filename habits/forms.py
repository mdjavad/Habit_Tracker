from django import forms 
from .models import Habit, User 
import bleach
from django.contrib.auth.hashers import make_password
        
class UserForm(forms.ModelForm):
    class Meta: 
        model = User
        fields = ['name', 'email', 'date_of_birth', 'password']

    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        return bleach.clean(name)

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return bleach.clean(email)

   
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class HabitForm(forms.ModelForm):
    class Meta: 
        model = Habit
        fields = '__all__'        



class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)


