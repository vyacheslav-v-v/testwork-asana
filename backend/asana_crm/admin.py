from django.contrib import admin

from asana_crm.models import Task, Project, AsanaUser


@admin.register(AsanaUser)
class Admin(admin.ModelAdmin):
    """ Админка пользователей Asana. """
    fields = ('name',)
    list_display = ('id', 'gid', 'name')
    list_filter = ('id', 'gid', 'name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """ Админка проектов Asana. """
    fields = ('name', 'workspace')
    list_display = ('id', 'gid', 'name', 'workspace')
    list_filter = ('id', 'gid', 'name')
    actions = ['delete_all_projects']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """ Админка задач Asana. """
    fields = ('name', 'assignee', 'projects', 'notes', 'workspace')
    list_display = ('id', 'gid', 'name', 'notes', 'assignee')
    list_filter = ('name', 'projects', 'notes', 'assignee')
    search_fields = ('notes', 'gid')
