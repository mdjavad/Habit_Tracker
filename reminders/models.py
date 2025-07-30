from django.db import models
from habits.models import Habit
from django.utils import timezone

class HabitReminder(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    last_reminded = models.DateTimeField(default=timezone.now)
    reminder_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.habit.name} - {self.reminder_time}"

