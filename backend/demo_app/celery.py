import os

from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_app.settings')

app = Celery('demo_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

DEFAULT_EXCHANGE_NAME = 'demo_app-celery-default'
DEFAULT_EXCHANGE_TYPE = 'topic'
DEFAULT_ROUTING_KEY = 'demo_app-celery-default'
DEFAULT_QUEUE_NAME = 'demo_app-celery-default'

DEFAULT_EXCHANGE = Exchange(
    name=DEFAULT_EXCHANGE_NAME,
    type=DEFAULT_EXCHANGE_TYPE
)

app.conf.task_queues = (
    Queue(
        DEFAULT_QUEUE_NAME,
        DEFAULT_EXCHANGE,
        routing_key=DEFAULT_ROUTING_KEY
    ),
)

app.conf.task_default_queue = DEFAULT_QUEUE_NAME
app.conf.task_default_exchange = DEFAULT_EXCHANGE
app.conf.task_default_routing_key = DEFAULT_ROUTING_KEY

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
