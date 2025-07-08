from django.db import models


class User(models.Model): 

           User_id = models.IntegerField() 
           name =  models.CharField(max_length=100) 
           email   =  models.EmailField()
           date_of_birth = models.DateField() 
           password = models.CharField(max_length=128) 
class habits(models.Model):
    Habit_id = models.IntegerField()
    User_id = models.IntegerField(models.ForeignKey("app.Model", verbose_name= (""), on_delete=models.CASCADE))
    Habit_name = models.CharField() 
    description = models.CharField()
    duration = models.DurationFieldField()
    reminder = models.AutoFill()
    
    class HabitLog(models.Model):
    id = models.IntegerField()
    habit_id = models.ForeignKey()
    date = models.DateField()
    status = models.CharField(max_length=50)
