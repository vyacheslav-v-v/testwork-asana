from unittest import mock

from django.test import TestCase

from asana_crm.api.client import AsanaApi
from asana_crm.models import Workspace
from asana_crm.tests.factories import (ProjectFactory, WorkspaceFactory)


class AsanaApiTestCase(TestCase):
    """ Проверка работы api Asana. """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        WorkspaceFactory()

    @mock.patch('asana.resources.workspaces.Workspaces.find_all')
    def test_sync_workspaces(self, find_all_mock):
        """ Синхронизацию рабочих пространств """
        Workspace.objects.all().delete()
        SERVER_WORKSPACES = [
            {'gid': '111111', 'name': 'first_workspace'},
            {'gid': '222222', 'name': 'second_workspace'},
        ]
        find_all_mock.return_value = SERVER_WORKSPACES

        AsanaApi().sync_workspaces()

        data = Workspace.objects.values('gid', 'name')
        self.assertEqual(SERVER_WORKSPACES, list(data))

    @mock.patch('asana.resources.projects.Projects.create')
    def test_create_project(self, create_mock):
        """ Отправка нового проекта. """
        project = ProjectFactory(gid=None)
        data = {'gid': None,
                'name': project.name,
                'workspace': project.workspace.gid}
        server_data = {'gid': '11111',
                       'name': project.name,
                       'workspace': {'gid': project.workspace.gid}}

        create_mock.return_value = server_data

        AsanaApi().send_project(project)

        project.refresh_from_db()
        create_mock.assert_called_once_with(data)
        self.assertEqual(project.gid, server_data['gid'])

    @mock.patch('asana.resources.projects.Projects.update')
    def test_update_project(self, update_mock):
        """ Отправка проекта, уже ранее отправлявшегося. """
        project = ProjectFactory(gid='22222')
        data = {'gid': project.gid,
                'name': project.name,
                'workspace': project.workspace.gid}
        server_data = {'gid': project.gid,
                       'name': project.name,
                       'workspace': {'gid': project.workspace.gid}}

        update_mock.return_value = server_data

        AsanaApi().send_project(project)

        update_mock.assert_called_once_with(data['gid'], data)

# Тесты написаны не в полном объёме, но принцип везде одинаковый.
# Также нет тестов эксепшенов при неудачи в задачах. Т.к. нет и самих
# эксепшенов. Грамотно написать эксепшены долго, но не сложно. В данном
# случае, за отсутствием документации, нужно исследовать исходники Asana
# python.
