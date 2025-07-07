from django.db import models

class User(models.Model): 

           User_id = models.IntegerField() 
           name =  models.CharField(max_length=100) 
           email   =  models.EmailField() 
           date_of_birth = models.DateField() 
           password = models.CharField(max_length=128) 
