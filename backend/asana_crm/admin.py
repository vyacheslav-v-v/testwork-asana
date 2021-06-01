from django.contrib import admin

from asana_crm.models import Task, Project, AsanaUser


@admin.register(AsanaUser)
class UserAdmin(admin.ModelAdmin):
    """User admin"""
    fields = ('name',)
    list_display = ('id', 'gid', 'name')
    list_filter = ('id', 'gid', 'name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Project admin"""
    fields = ('name', 'workspace')
    list_display = ('id', 'gid', 'name', 'workspace')
    list_filter = ('id', 'gid', 'name')
    actions = ['delete_all_projects']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Task admin"""
    fields = ('name', 'assignee', 'projects', 'notes', 'workspace')
    list_display = ('id', 'gid', 'name', 'notes', 'assignee')
    list_filter = ('name', 'projects', 'notes', 'assignee')
    search_fields = ('notes', 'gid')
