from __future__ import absolute_import, unicode_literals

# Certifique-se de que o Celery é importado quando o Django inicia
from .celery import app as celery_app

__all__ = ('celery_app',)
