from django.apps import AppConfig


class HabitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'habits'
from django.apps import AppConfig

class HabitsConfig(AppConfig):
    name = 'habits'

    def ready(self):
        from . import scheduler
        scheduler.start()