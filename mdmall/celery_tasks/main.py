from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mdmall.settings')

celery_app = Celery('my_tasks', broker='redis://127.0.0.1:6379/4')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks(['celery_tasks.send_email', 'celery_tasks.haystack_rebuild', 'celery_tasks.upload_file'])














