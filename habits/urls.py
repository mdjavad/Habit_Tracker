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
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),
    path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
     path('send/' , views.send),

]