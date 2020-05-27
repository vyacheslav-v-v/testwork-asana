import logging
import pprint

from django.conf import settings

from asana_crm.api.client import AsanaApi
from asana_crm.models import Project, Task
from demo_app.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def send_project(self, project_id):
    """ Задача отправки проекта в Asana.

    Максимально упрощённо.
    """
    project = Project.objects.get(id=project_id)
    try:
        if not settings.TESTING:
            AsanaApi().send_project(project)
    except Exception as e:
        error_message = ('Can`t send the project to Asana: %s',
                         pprint.saferepr(e))
        logger.exception(error_message)
        raise self.retry(exc=e, countdown=2 ** (self.request.retries + 5))


@app.task(bind=True)
def send_task(self, task_id):
    """ Задача отправки задачи в Asana. """
    task = Task.objects.get(id=task_id)
    try:
        if not settings.TESTING:
            AsanaApi().send_task(task)
    except Exception as e:
        error_message = ('Can`t send the task to Asana: %s',
                         pprint.saferepr(e))
        logger.exception(error_message)
        raise self.retry(exc=e, countdown=2 ** (self.request.retries + 5))


@app.task(bind=True)
def sync_additional_objects(self):
    """ Получаем пользователей и рабочие области. """
    if not settings.TESTING:
        client = AsanaApi()
        client.sync_users()
        client.sync_workspaces()
