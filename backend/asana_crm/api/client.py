import logging

import asana
from django.conf import settings

from asana_crm.api.serializers import (
    WorkspaceSerializer, AsanaUserSerializer, ProjectSerializer, TaskSerializer
)
from asana_crm.models import Workspace, Task

logger = logging.getLogger(__name__)


class AsanaApi:
    """ Класс для работы с API Asana.

    Здесь отсутствуют кастомные исключения, их нужно обязательно добавить и
    использовать в реальном проекте.
    """
    _client = None
    _workspace = None

    def __init__(self) -> None:
        AsanaApi._client = self._get_client()

    def get_default_workspace(self):
        """ Берём первый попавшийся workspace.

        Делаем просто чтобы работало.
        """
        if not self._workspace:
            self._workspace = Workspace.objects.get(gid__isnull=False)
        return self._workspace

    def _get_client(self):
        """ Получение клиента. """
        return asana.Client.access_token(settings.ASANA_ACCESS_TOKEN)

    def sync_workspaces(self):
        """ Синхронизация рабочих областей.

        Только загружаем области.
        """
        client = self._client
        workspaces = client.workspaces.find_all()
        for workspace in workspaces:
            instance = Workspace.objects.filter(gid=workspace['gid']).first()
            ws_serializer = WorkspaceSerializer(instance=instance,
                                                data=workspace)
            # Здесь должен быть перехват исключения и вызов своего эксепшена.
            ws_serializer.is_valid(raise_exception=True)
            ws_serializer.save()

    def sync_users(self):
        """ Синхронизация пользователей.

        Очень плохо, код дублируется. Но этого в задании не требовалось,
        поэтому оставляю как есть.
        """
        client = self._client
        users = client.users.find_all(
            {'workspace': self.get_default_workspace().gid},
        )
        for user in users:
            instance = Workspace.objects.filter(gid=user['gid']).first()
            user_serializer = AsanaUserSerializer(instance=instance,
                                                  data=user)
            # Упрощаем, не обрабатываем ошибки.
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

    def send_project(self, project):
        """ Отправка проекта в Asana. """
        client = self._client
        # Если в проекте не установлен синхронизированный workspace,
        # устанавливаем workspace по умолчанию.
        if not project.workspace or not project.workspace.gid:
            project.workspace = self.get_default_workspace()
        data = ProjectSerializer(instance=project).data
        if project.gid:
            client.projects.update(data['gid'], data)
        else:
            gid = client.projects.create(data)['gid']
            # Сохраняем gid.
            project.set_gid(gid)

    def send_task(self, task):
        """ Отправка задачи в Asana.

        Здесь нужно выполнить проверку, что связанные объекты синхронизированы
        и, если нет, либо их синхронизировать, либо запланировать повтор
        задачи в расчёте что они синхронизируются в другом месте.
        """
        client = self._client
        data = TaskSerializer(instance=task).data
        # Если задача уже синхронизировалась - обновляем
        if task.gid:
            # Убираем проекты из запроса проекты, asana не позволяет установить
            # их напрямую
            data.pop('projects')
            new_data = client.tasks.update(task.gid, data)
            self.sync_task_groups(task, new_data)
        else:
            # Если это новая задача - создаём на сервере в основном рабочем
            # пространстве.
            data['workspace'] = self.get_default_workspace().gid
            gid = client.tasks.create(data)['gid']
            # Сохраняем gid.
            task.set_gid(gid)

    def sync_task_groups(self, task: Task, remote_data: dict = None):
        """ Синхронизация проектов задачи. """
        remote_data = remote_data or self._get_task_data(task.gid)
        l_projects = set(task.projects.values_list('gid', flat=True))
        r_projects = {p['gid'] for p in remote_data['projects']}

        # Добавляем отсутствующие в asana проекты.
        for project_gid in l_projects - r_projects:
            self._client.tasks.add_project(task.gid, {'project': project_gid})

        # Удаляем проекты, присутствующие в Asana, но отсутствующие у нас.
        for project_gid in r_projects - l_projects:
            self._client.tasks.remove_project(task.gid,
                                              {'project': project_gid})

    def _get_task_data(self, gid) -> dict:
        """ Получаем данные задачи с сервера."""
        return self._client.tasks.find_by_id(gid)

    def delete_all_projects(self):
        """ Удаляем все проекты. """
        client = self._client
        workspaces = client.workspaces.find_all()
        for workspace in workspaces:
            projects = client.projects.find_by_workspace(workspace['gid'])
            for project in projects:
                client.projects.delete(project['gid'])
