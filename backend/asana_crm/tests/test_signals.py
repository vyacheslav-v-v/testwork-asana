from unittest import mock

from django.test import TestCase

from asana_crm.models import Project


class SendAsanaDataSignalsTestCase(TestCase):
    """ Проверяем запуск отправки данных в Asana после изменения сущностей.

    Сигналы должны запускать celery-таски.
    """

    @mock.patch('asana_crm.signals.transaction.on_commit')
    def test_signal_send_project(self, mock_on_commit):
        """ Проверяем запуск таски сигналом при создании проекта. """
        Project.objects.create()
        mock_on_commit.assert_called_once()

    @mock.patch('asana_crm.signals.transaction.on_commit')
    def test_signal_send_task(self, mock_on_commit):
        """ Проверяем запуск таски сигналом при создании задачи. """
        mock_on_commit.reset_mock()
        Project.objects.create()
        mock_on_commit.assert_called_once()
