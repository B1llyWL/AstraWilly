import os
from celery import Celery

# Устанавливаем модуль настроек Django по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('astrawilly')

# Загружаем конфигурацию из настроек Django, используя пространство имен CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в приложениях
app.autodiscover_tasks()