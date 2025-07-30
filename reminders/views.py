from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import HabitReminder
from .forms import ReminderTimeForm
from habits.models import Habit

def reminder_list(request):
    reminders = HabitReminder.objects.select_related('habit__user')
    return render(request, 'reminder_list.html', {'reminders': reminders})

def edit_reminder(request, reminder_id):
    reminder = get_object_or_404(HabitReminder, id=reminder_id)

    if request.method == 'POST':
        form = ReminderTimeForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('reminder_list')
    else:
        form = ReminderTimeForm(instance=reminder)

    return render(request, 'edit_reminder.html', {'form': form, 'reminder': reminder})


def set_reminder(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    reminder, created = HabitReminder.objects.get_or_create(habit=habit)

    if request.method == 'POST':
        form = ReminderTimeForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReminderTimeForm(instance=reminder)

    return render(request, 'set_reminder.html', {'form': form, 'habit': habit})
