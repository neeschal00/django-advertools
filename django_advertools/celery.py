import os
from celery import Celery
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_advertools.settings")

app = Celery("django_advertools")

# Using a string here means the worker doesn't
# have to serialize the configuration object to
# child processes. - namespace='CELERY' means all
# celery-related configuration keys should
# have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# celery.py (or wherever you configure Celery)
# app.conf.beat_schedule = {
#     'flower-stats': {
#         'task': 'flower.commands.stats',
#         'schedule': timedelta(seconds=5),
#         'options': {'queue': 'flower'},
#     },
# }


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
