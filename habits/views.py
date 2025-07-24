from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, User, PasswordReset
from .forms import HabitForm, UserForm, LoginForm
from django.contrib import messages
from .decorators import role_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
 

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Register successfully')
            return redirect('home')
    else:
        form = UserForm() 
    return render(request, 'register.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.filter(name=username).first()
                if user and check_password(password, user.password):
                    request.session['user_id'] = user.id
                    messages.success(request, 'login successfully')
                    return redirect('home')
                else:
                    form.add_error(None, 'Invalid username or password')
            except User.DoesNotExist:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


    

def logout_user(request):
    request.session.flush()
    return redirect('login')

def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER, 
                [email]  
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'forgot_password.html')

def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
       
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

def ResetPassword(request, reset_id):
  try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.password = make_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('home')
            else:
                
                return redirect('reset-password', reset_id=reset_id)

    
  except PasswordReset.DoesNotExist:
        
       
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

  return render(request, 'reset_password.html')

def dashboard(request):
    return redirect('login')

@role_required('Admin', 'Manager', 'Developer') 
def home(request):
  user_id = request.session.get('user_id')
  if not user_id:
      return redirect('login')
  
  habits = Habit.objects.filter(user_id=user_id)
  return render(request, 'home.html', {'habits': habits})

def Habit_view(request, pk):
   Habits = Habit.objects.get(pk=pk)
   return render(request, 'Habit.html', {'Habits': Habits} )
    


def CreateHabit(request):
     form = HabitForm() 

     if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
     context = {'form': form}
     return render(request, 'Habit_form.html', context)

def UpdateHabit(request, pk):
    habit = Habit.objects.get(pk=pk)
    form = HabitForm(instance=habit)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'Habit_form.html', context)



def DeleteHabit(request, pk):
      habit = Habit.objects.get(pk=pk)
   
      if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
      
        habit.delete()
        return redirect('home')

   
      return render(request, 'delete.html', {'obj':Habit})