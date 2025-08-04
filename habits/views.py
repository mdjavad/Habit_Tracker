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
from reminders.models import HabitReminder
from django.http import HttpResponse
import requests
import json


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

    for habit in habits:
        try:
            habit.reminder = HabitReminder.objects.get(habit=habit)
        except HabitReminder.DoesNotExist:
            habit.reminder = None

    return render(request, 'home.html', {'habits': habits})

  
 

def Habit_view(request, pk):
    Habits = get_object_or_404(Habit, pk=pk)

    try:
        Habits.reminder = HabitReminder.objects.get(habit=Habits)
    except HabitReminder.DoesNotExist:
        Habits.reminder = None

    return render(request, 'Habit.html', {'Habits': Habits})

    


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

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyAdGLgTWNFB91sq_3vascE_E-Z4_dshBxU",' \
         '        authDomain: "habit-tracker-2a428.firebaseapp.com",' \
         '        projectId: "habit-tracker-2a428",' \
         '        storageBucket: "habit-tracker-2a428.firebasestorage.app",' \
         '        messagingSenderId: "890703119462",' \
         '        appId: "1:890703119462:web:6aa6ad70f36548af5359a7",' \
         '        measurementId: "G-EDY64CGP50"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")


def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCNkcP0Wh4w5Q6F\nxhCjf4C/MUlPyQhl86uWo8WnxfFIJ8pXrfLiKhiTwcLxcFbi/nbrUt4HLB6YQ9Vd\nOPs8eFEKK5aj8+C47ngwgBlO8RBVhuN9MXOkStYqt89A6cYTfsaOUa2mvae3MTYG\nzInLtMK0NBFE5iaxafRQIPLloy4OoZ2Ggn3hqKqGIbAA+ZFZq1oqe+hycNezTMgr\nzb8pyjnO1u7KvGGxofDlqn/G07o5iftw2kBYIhRrPw+GIGuf7eB2gG+uqPWstEY8\nNb6jfN+wEV/D8uPUHx3mK/5oX8dp91/u57NkZpuMUS0j2373yGli1Usj9jAHZp4w\nRVGZ0wZJAgMBAAECggEADcDc5YTpRLUGEok11dp12K06OvPz+sqfz4JQ2h4k9Q53\njgnWTDJMgbNL4+6W5FXWGgHKk+4NeVuys2wtHThvoBIwv/QaD4FMYCLbwpNxE6wH\ndwLKQipqkMsbaYokjgGNmuc0vHuVmvqfDe1KUEXa+gyKZnQJC4iYfX3b9yMBnxZf\noKvagV776ce1Ulwlb8joUl6zLBdFyAZ8GesxsHIjtge7uQQGvxgV+8W5mAFUgy8s\nEwzHuod0TUQZhdy4jxayJNPLsMP1WUbRd4EG2cUDs4N/OWMHmzo2NuFHLgAmV3by\n/Okbu315bzCCu72qGIvIuIpgDUF42xY4/WuqEpyU8QKBgQDEIz5h6oe40gLoUJrO\n0WG0NKO1heIjYFBzUtNVYV1ejAbdY6c99FFkuQWm0OXxIOCYlQZKMjQINP+XJR9H\nMmM8h+vW7psWLxDJ6Al0dcfxUAiS/klVGBan4k7w6rvhB8Rf9dseVyZ2vXDX1nZp\nF6+Pf6TrXVKWuVONOoTmzlDxMQKBgQC4xvUxl+LbPy4cPSPZHfVl4KdrdcUTbzx6\nd1S58TQAPZfNOEUz8EPaj467wBFweiI/EdAuSU4/U+FXa3vkCYikBYBi6LqP70KQ\ndIAmTQ3tjgT7CUWpKTcmZPI+uCzOCbrMtpDyVKMDdscLoDzb2LvYFIKpTR6AIJdH\nCLvUJOjgmQKBgQCvipeHjR9Bo/xkLdgP6EfYwBARI61cWhRG0sdAMC8fspVmSY1i\nHqtGSW4seeSCphk9losVls8I1V43yUqwLwGwKDpEmDMHbMJK4rirmcqESEwUOzAo\nz7FfOmXKq1vRsGDqPaGKCxfqx+wZ0OETd9ZxyR0yZcjIC0AjM0/FPrwk0QKBgBov\nH3naoywchOU9iMHwq+C2+CKTOs0pOzHDjT8YPh02nTdYnP3iM0tagoh6jD4bIJU9\nafnVK4Bv24Pu2EyVSUas/OeHQUC6T/12dN54ltut/2ivhK6XB5iqP2XB5Z+A43a0\n/E9KzRrljwlHuLgSu3PAXE+vfP39IFLRmwRSAqopAoGBAI1EjFepx391RtpwFcU6\nQjPIpRiUud1B9LhB8jLMsQ5Fz8FKqoWSIg4UkO8lq753ugKT2Eg1Mt5MfOSeqWrA\nz4H1KTNOvNiolnbr62CymlAUDhehlRxOizx6TmqtRoEyFYH41cSqYO+zrZmGjXYL\nzsuSEUblPoCCkNOXIgaNTVAt"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())

def send(request):
    resgistration  = ['mJ1O5JlvPcl3_yFB11JS5:APA91bF40mp1NpGLVB7wGkUK0xIkZ-INHfOofTmHOffYrN5iGPX9CLl1VNEJV6HR66-5BeJm0c34-EmbMEGam78k3cqWNJjI6i8CPltbzs4oIQzYqUzJiRQ'
    ]
    send_notification(resgistration , 'Reminder for Habit ' , 'Habit Tracker ')
    return HttpResponse("sent")