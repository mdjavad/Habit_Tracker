from django.db import models

class habits(models.Model):
    Habit_id = models.IntegerField()
    User_id = models.IntegerField(models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE))
    Habit_name = models.CharField() 
    description = models.CharField()
    duration = models.DurationFieldField()
    reminder = models.AutoField()