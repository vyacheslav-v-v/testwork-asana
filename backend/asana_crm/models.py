from django.db import models

from tools.models import nullable
from users.models import User


class SyncStatusAbstract(models.Model):
    NEED_SYNC = 'need sync'
    SYNCED = 'synced'

    SYNC_STATUSES = (
        (NEED_SYNC, 'Object changed, synchronization required'),
        (SYNCED, 'Synchronized'),
    )

    sync_status = models.CharField('Synchronization status',
                                   default=NEED_SYNC, max_length=11,
                                   choices=SYNC_STATUSES)

    gid = models.CharField('gid', max_length=50, db_index=True, unique=True,
                           **nullable)

    def change_status(self, status) -> None:
        """Changes synchronization status."""
        if status != self.sync_status:
            self.__class__.objects.filter(id=self.id).update(status=status)

    def set_gid(self, gid):
        self.__class__.objects.filter(id=self.id).update(gid=gid)

    class Meta:
        abstract = True
        verbose_name = 'Synchronization status'
        verbose_name_plural = 'Synchronization statuses'


class Workspace(SyncStatusAbstract):
    """Asana workspace."""
    name = models.CharField('Имя', max_length=255)

    def __str__(self):
        return f'Рабочее пространство {self.id} {self.name}'

    class Meta:
        verbose_name = 'Рабочая область'
        verbose_name_plural = 'Рабочие области'


class AsanaUser(SyncStatusAbstract):
    """Asana user.

    It is not known whether Asana and Django users will overlap, so we make
    a separate model and do not make reference fields to the User model.
    """
    name = models.CharField('name', max_length=255, db_index=True)

    def __str__(self):
        return f'Asana user {self.id} {self.name}'

    class Meta:
        verbose_name = 'Asana user'
        verbose_name_plural = 'Asana users'


class Project(SyncStatusAbstract):
    """Asana project."""
    name = models.CharField('name', max_length=255)
    workspace = models.ForeignKey(Workspace, related_name='projects',
                                  on_delete=models.CASCADE, **nullable)

    def __str__(self):
        return f'Project {self.id} {self.name}'

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class Task(SyncStatusAbstract):
    """Asana project task."""
    name = models.CharField('name', max_length=255)
    projects = models.ManyToManyField(Project, related_name='tasks',
                                      blank=True)
    notes = models.TextField('содержание', **nullable)
    assignee = models.ForeignKey(AsanaUser, related_name='tasks',
                                 on_delete=models.CASCADE, **nullable)
    workspace = models.ForeignKey(Workspace, related_name='tasks',
                                  on_delete=models.CASCADE, **nullable)

    def __str__(self):
        return f'Task {self.id} {self.name}'

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
