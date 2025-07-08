from django.contrib import admin

from .models import User, Habit, HabitLog

admin.site.register(User)
admin.site.register(Habit)
admin.site.register(HabitLog)
