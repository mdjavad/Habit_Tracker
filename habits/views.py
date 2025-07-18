from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, User 
from .forms import HabitForm, UserForm, LoginForm
from django.contrib import messages

 

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
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
                user = User.objects.get(name=username, password=password)
                request.session['user_id'] = user.id
                return redirect('home')
            except User.DoesNotExist:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

    

def logout_user(request):
    request.session.flush()
    return redirect('login')

def dashboard(request):
    return redirect('login')

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


