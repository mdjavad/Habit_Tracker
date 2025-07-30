from django.urls import path
from .views import reminder_list, edit_reminder, set_reminder

urlpatterns = [
    path('reminders/', reminder_list, name='reminder_list'),
    path('reminders/<int:reminder_id>/edit/', edit_reminder, name='edit_reminder'),
    path('set-reminder/<int:habit_id>/', set_reminder, name='set_reminder'),

]
