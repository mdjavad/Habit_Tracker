from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
     path('register/', views.register_user, name="register"),
    path('', views.home, name="home"),
    path('Habit/<str:pk>/', views.Habit_view, name="Habit"),
     path('create-habit/', views.CreateHabit, name="Create-Habit"),
     path('Update-habit/<str:pk>/', views.UpdateHabit, name="Update-habit"),
     path('delete-habit/<str:pk>/', views.DeleteHabit, name="delete-habit"),

]