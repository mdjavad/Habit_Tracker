from django.urls import path
from . import views

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────
    path('',                views.home,          name='home'),
    path('register/',       views.register_user, name='register'),
    path('login/',          views.login_user,    name='login'),
    path('logout/',         views.logout_user,   name='logout'),

    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<uuid:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<uuid:reset_id>/',      views.ResetPassword,     name='reset-password'),

    # ── Habits — all name variants your templates might use ──
    path('habits/create/',  views.CreateHabit, name='Create-Habit'),
    path('habits/new/',     views.CreateHabit, name='create-habit'),    # alias
    path('habits/add/',     views.CreateHabit, name='add-habit'),       # alias

    path('habits/<int:pk>/',          views.Habit_view,  name='Habit'),
    path('habits/<int:pk>/view/',     views.Habit_view,  name='habit-detail'),  # alias

    path('habits/<int:pk>/update/',   views.UpdateHabit, name='Update-habit'),
    path('habits/<int:pk>/edit/',     views.UpdateHabit, name='UpdateHabit'),   # alias
    path('habits/<int:pk>/change/',   views.UpdateHabit, name='update-habit'),  # alias

    path('habits/<int:pk>/delete/',   views.DeleteHabit, name='Delete-habit'),
    path('habits/<int:pk>/remove/',   views.DeleteHabit, name='DeleteHabit'),   # alias
    path('habits/<int:pk>/destroy/',  views.DeleteHabit, name='delete-habit'),  # alias

    path('habits/<int:pk>/complete/', views.complete_habit_today, name='complete-habit'),

    # ── OneSignal ─────────────────────────────────────────
    path('save-player-id/',    views.save_onesignal_player, name='save-player-id'),
    path('test-notification/', views.send,                  name='test-notification'),
]