from typing import Mapping

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.encoding import smart_str
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.relations import RelatedField

from asana_crm.models import Workspace, AsanaUser, Project, Task


class GidRelatedField(RelatedField):
    """ Поле, позволяющее устанавливать отношения между моделями по gid. """
    default_error_messages = {
        'does_not_exist': 'Объект {value["gid"]} не существует.',
        'invalid': 'Неверное значение.',
    }

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(gid=data['gid'])
        except ObjectDoesNotExist:
            self.fail('does_not_exist', value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        return obj.gid


class WorkspaceSerializer(serializers.ModelSerializer):
    """ Сериалайзер рабочих областей. """

    class Meta:
        model = Workspace
        fields = ['gid', 'name']


class AsanaUserSerializer(serializers.ModelSerializer):
    """ Сериалайзер пользователей Asana. """

    class Meta:
        model = AsanaUser
        fields = ['gid', 'name']

    def __init__(self, instance=None, data=empty, **kwargs):
        if not instance and isinstance(data, Mapping):
            try:
                instance = self.Meta.model.objects.get(gid=data['gid'])
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                pass

        super().__init__(instance, data, **kwargs)


class ProjectSerializer(serializers.ModelSerializer):
    """ Сериалайзер проектов Asana. """
    workspace = GidRelatedField(queryset=Workspace.objects.all())

    class Meta:
        model = Project
        fields = ['gid', 'name', 'workspace']


class TaskSerializer(serializers.ModelSerializer):
    """ Сериалайзер задач Asana. """
    projects = GidRelatedField(many=True, queryset=Project.objects.all())
    assignee = GidRelatedField(queryset=AsanaUser.objects.all(),
                               allow_null=True)

    class Meta:
        model = Task
        fields = ['gid', 'name', 'projects', 'notes', 'assignee', ]
