from django.db import models

class User(models.Model): 
    name = models.CharField(max_length=100) 
    email = models.EmailField()
    date_of_birth = models.DateField() 
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    description = models.TextField()
    duration = models.DurationField()
    reminder = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.habit.name} - {self.date}"
