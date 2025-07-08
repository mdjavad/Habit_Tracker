from django.db import models

class HabitLog(models.Model):
    id = models.IntegerField()
    habit_id = models.ForeignKey()
    date = models.DateField()
    status = models.CharField(max_length=50)