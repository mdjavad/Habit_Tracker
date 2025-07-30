from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from reminders.models import HabitReminder

class Command(BaseCommand):
    help = 'Send habit reminder emails'

    def handle(self, *args, **kwargs):
        now = timezone.localtime()  # ✅ get current local time

        reminders = HabitReminder.objects.select_related('habit__user')

        for reminder in reminders:
            reminder_time = reminder.reminder_time

            # ✅ Add this line to debug time matching:
            print(f"Checking: {reminder.habit.name} at {reminder_time} vs now {now.time()}")

            # Compare current time vs reminder time (in minutes)
            now_minutes = now.hour * 60 + now.minute
            reminder_minutes = reminder_time.hour * 60 + reminder_time.minute

            if abs(now_minutes - reminder_minutes) <= 5:
                user = reminder.habit.user
                habit = reminder.habit

                try:
                    send_mail(
                        'Habit Reminder',
                        f"Hey {user.name}, remember to do your habit: {habit.name}",
                        'noreply@habittracker.com',
                        [user.email],
                        fail_silently=False,
                    )
                    reminder.last_reminded = timezone.now()
                    reminder.save()

                    self.stdout.write(self.style.SUCCESS(
                        f"✅ Reminder sent to {user.email} for habit '{habit.name}'"
                    ))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"❌ Failed to send to {user.email}: {str(e)}"
                    ))
