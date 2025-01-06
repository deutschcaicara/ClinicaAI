from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configurações do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClinicaAI.settings')

app = Celery('ClinicaAI')

# Configurações do Celery no arquivo settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobrir automaticamente tarefas em apps instalados
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
