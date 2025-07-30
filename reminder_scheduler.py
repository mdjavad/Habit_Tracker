import os
import django
import schedule
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Habit_Tracker.settings')
django.setup()

from django.core.management import call_command

def run_reminder_command():
    print("Running send_reminders...")
    call_command('send_reminders')

# Run every 1 minute
schedule.every(1).minutes.do(run_reminder_command)

print("⏰ Reminder scheduler is running...")

while True:
    schedule.run_pending()
    time.sleep(1)
