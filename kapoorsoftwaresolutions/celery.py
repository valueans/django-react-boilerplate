from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kapoorsoftwaresolutions.settings")

app = Celery("kapoorsoftwaresolutions")
app.conf.enable_utc = False
app.conf.update(timezone=settings.TIME_ZONE)

app.config_from_object(settings, namespace="CELERY")

app.conf.beat_schedule = {
    # daily database backup
    "database-backup": {
        "task": "users.tasks.databaseBackupDaily",
        "schedule": crontab(hour=5, minute=00),
    }
}


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
