from django.db import models
from django.contrib.auth.models import User 
from django.db.models.deletion import CASCADE
import uuid

class User(models.Model): 
    name = models.CharField(max_length=100) 
    email = models.EmailField()
    date_of_birth = models.DateField() 
    password = models.CharField(max_length=128)
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Developer', 'Developer'),
        ('Manager', 'Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Developer')

    def __str__(self):
        return self.name

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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
    
class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"

