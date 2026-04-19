from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)

def send_daily_reminders():
    """Called every day at 8 AM IST — sends reminders to all subscribed users."""
    from .models import User, Habit
    from .views import send_notification

    users = User.objects.exclude(onesignal_player_id__isnull=True).exclude(onesignal_player_id='')
    logger.info(f'Sending reminders to {users.count()} users')

    for user in users:
        habit_count = Habit.objects.filter(user=user).count()
        if habit_count > 0:
            send_notification(
                player_ids=[user.onesignal_player_id],
                message_title='🔔 Daily Habit Reminder',
                message_desc=f'You have {habit_count} habit(s) to complete today!'
            )

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_daily_reminders,
        CronTrigger(hour=8, minute=0, timezone='Asia/Kolkata'),  # 8:00 AM IST daily
        id='daily_habit_reminder',
        replace_existing=True,
    )
    scheduler.start()
    logger.info('Habit reminder scheduler started — fires daily at 8:00 AM IST')