import logging

import asana
from django.conf import settings

from asana_crm.api.serializers import (
    WorkspaceSerializer, AsanaUserSerializer, ProjectSerializer, TaskSerializer
)
from asana_crm.models import Workspace, Task

logger = logging.getLogger(__name__)


class AsanaApi:
    """Class for working with the Asana API.

    Here are no custom exceptions. They should be added in a real project.
    """
    _client = None
    _workspace = None

    def __init__(self) -> None:
        AsanaApi._client = self._get_client()

    def get_default_workspace(self):
        """Get the first workspace.

        Just so that works.
        """
        if not self._workspace:
            self._workspace = Workspace.objects.get(gid__isnull=False)
        return self._workspace

    def _get_client(self):
        """Get client."""
        return asana.Client.access_token(settings.ASANA_ACCESS_TOKEN)

    def sync_workspaces(self):
        """Synchronize workspaces.

        Load workspaces only.
        """
        client = self._client
        workspaces = client.workspaces.find_all()
        for workspace in workspaces:
            instance = Workspace.objects.filter(gid=workspace['gid']).first()
            ws_serializer = WorkspaceSerializer(instance=instance,
                                                data=workspace)
            # Exception catcher should be here and it must raise the custom exception..
            ws_serializer.is_valid(raise_exception=True)
            ws_serializer.save()

    def sync_users(self):
        """Synchronize users."""
        client = self._client
        users = client.users.find_all(
            {'workspace': self.get_default_workspace().gid},
        )
        for user in users:
            instance = Workspace.objects.filter(gid=user['gid']).first()
            user_serializer = AsanaUserSerializer(instance=instance,
                                                  data=user)
            # Simplifying, not handling errors.
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

    def send_project(self, project):
        """Send logs to Asana."""
        client = self._client
        # If the project does not have a synchronized workspace installed,
        # set the default workspace.
        if not project.workspace or not project.workspace.gid:
            project.workspace = self.get_default_workspace()
        data = ProjectSerializer(instance=project).data
        if project.gid:
            client.projects.update(data['gid'], data)
        else:
            gid = client.projects.create(data)['gid']
            # Store gid.
            project.set_gid(gid)

    def send_task(self, task):
        """Send the task to Asana.

        Here you need to check that the related objects are synchronized and,
        if not, either synchronize them, or schedule a repeat of the task in
        the expectation that they will be synchronized elsewhere.
        """
        client = self._client
        data = TaskSerializer(instance=task).data
        # If the task has already been synchronized then refresh
        if task.gid:
            # We remove projects from the request, asana does not allow you
            # to set them directly
            data.pop('projects')
            new_data = client.tasks.update(task.gid, data)
            self.sync_task_groups(task, new_data)
        else:
            # If this is a new task then create it at the default workspace
            # on the server.
            data['workspace'] = self.get_default_workspace().gid
            gid = client.tasks.create(data)['gid']
            # Сохраняем gid.
            task.set_gid(gid)

    def sync_task_groups(self, task: Task, remote_data: dict = None):
        """Synchronize task projects."""
        remote_data = remote_data or self._get_task_data(task.gid)
        l_projects = set(task.projects.values_list('gid', flat=True))
        r_projects = {p['gid'] for p in remote_data['projects']}

        # Add missing projects to asana.
        for project_gid in l_projects - r_projects:
            self._client.tasks.add_project(task.gid, {'project': project_gid})

        # We delete projects that are present in Asana, but we do not have.
        for project_gid in r_projects - l_projects:
            self._client.tasks.remove_project(task.gid,
                                              {'project': project_gid})

    def _get_task_data(self, gid) -> dict:
        """Get task data from the server."""
        return self._client.tasks.find_by_id(gid)

    def delete_all_projects(self):
        """Remove all projects."""
        client = self._client
        workspaces = client.workspaces.find_all()
        for workspace in workspaces:
            projects = client.projects.find_by_workspace(workspace['gid'])
            for project in projects:
                client.projects.delete(project['gid'])
