from django.db import models

from tools.models import nullable
from users.models import User


class SyncStatusAbstract(models.Model):
    NEED_SYNC = 'need sync'
    SYNCED = 'synced'

    SYNC_STATUSES = (
        (NEED_SYNC, 'Объект изменён, требуется синхронизация'),
        (SYNCED, 'Синхронизирован'),
    )

    sync_status = models.CharField('Статус синхронизации',
                                   default=NEED_SYNC, max_length=11,
                                   choices=SYNC_STATUSES)

    gid = models.CharField('gid', max_length=50, db_index=True, unique=True,
                           **nullable)

    def change_status(self, status) -> None:
        """Изменяет статус синхронизации. """
        if status != self.sync_status:
            self.__class__.objects.filter(id=self.id).update(status=status)

    def set_gid(self, gid):
        self.__class__.objects.filter(id=self.id).update(gid=gid)

    class Meta:
        abstract = True
        verbose_name = 'Статус синхронизации'
        verbose_name_plural = 'Статусы синхронизации'


class Workspace(SyncStatusAbstract):
    """ Рабочая область проекта Asana. """
    name = models.CharField('Имя', max_length=255)

    def __str__(self):
        return f'Рабочее пространство {self.id} {self.name}'

    class Meta:
        verbose_name = 'Рабочая область'
        verbose_name_plural = 'Рабочие области'


class AsanaUser(SyncStatusAbstract):
    """ Пользователи проекта Asana.

    Неизвестно будут ли пользователи Asana и Django пересекаться, поэтому
    делаем отдельную модель и не делаем ссылочных полей на модель User.
    """
    name = models.CharField('Имя', max_length=255, db_index=True)

    def __str__(self):
        return f'Пользователь Asana {self.id} {self.name}'

    class Meta:
        verbose_name = 'Пользователь Asana'
        verbose_name_plural = 'Пользователи Asana'


class Project(SyncStatusAbstract):
    """ Проект Asana. """
    name = models.CharField('наименование', max_length=255)
    workspace = models.ForeignKey(Workspace, related_name='projects',
                                  on_delete=models.CASCADE, **nullable)

    def __str__(self):
        return f'Проект {self.id} {self.name}'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Task(SyncStatusAbstract):
    """ Задача проекта Asana. """
    name = models.CharField('наименование', max_length=255)
    projects = models.ManyToManyField(Project, related_name='tasks',
                                      blank=True)
    notes = models.TextField('содержание', **nullable)
    assignee = models.ForeignKey(AsanaUser, related_name='tasks',
                                 on_delete=models.CASCADE, **nullable)
    workspace = models.ForeignKey(Workspace, related_name='tasks',
                                  on_delete=models.CASCADE, **nullable)

    def __str__(self):
        return f'Задача {self.id} {self.name}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
