import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")

app = Celery("shop")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'every': {
        'task': 'catalog.tasks.some_scheduled_task',
        'schedule': 5.0,
    },
}