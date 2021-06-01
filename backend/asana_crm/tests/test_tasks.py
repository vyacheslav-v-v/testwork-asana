from unittest import mock

from django.test import TestCase, override_settings

from asana_crm import tasks
from asana_crm.models import Task, Project


class AsanaTasksTestCase(TestCase):
    """" Тесты задач по синхронизации с Asana"""

    @mock.patch('asana_crm.tasks.AsanaApi.send_project')
    def test_send_project_task(self, api_send_project):
        """ Вызов Celery-таской отправки проекта к API. """
        project = Project.objects.create()

        with override_settings(TESTING=False):
            tasks.send_project.delay(project.id)

        api_send_project.assert_called_once_with(project)

    @mock.patch('asana_crm.tasks.AsanaApi.send_task')
    def test_send_task_task(self, api_send_task):
        """ Вызов Celery-таской отправки задачи к API. """
        task = Task.objects.create()

        with override_settings(TESTING=False):
            tasks.send_task.delay(task.id)

        api_send_task.assert_called_once_with(task)
