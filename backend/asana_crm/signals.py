from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from asana_crm import tasks
from asana_crm.models import Project, Task


# There is a lack of project synchronization when changing the scope of
# projects for a task or the scope of tasks programmatically without
# re-saving the task.
# To handle this, you need to intercept the m2m_changed signal from the
# Task.projects.through sender.

# It is also advisable to handle cases when an object is re-saved without
# actually changing it. In this case, there is no need to do synchronization.
# But it should also be borne in mind that when oversaving, the
# Task.projects.set () or Project.tasks.set () methods can be called, which
# call signals with the pre_clear and post_add actions
# It is possible in the pre_clear actions to save the list of current
# projects for the task, or the list of tasks for the project in the instance
# and then, when receiving a signal from the post_add action, compare the old
# and new lists to determine if anything has changed.

@receiver(post_save, sender=Project, dispatch_uid='send_project_uid')
def send_project(sender, instance, **kwargs):
    """Update the data in Asana when creating or editing a project."""
    # We are still in an uncompleted transaction. Therefore, if we create
    # a task directly, the worker can pick it up before the commit occurs.
    # In this case, we can send non-relevant data to Asana, or, if this is
    # a new project, the task may not find it at all. To exclude this we
    # use on_commit.
    transaction.on_commit(lambda: tasks.send_project.delay(instance.id))


@receiver(post_save, sender=Task, dispatch_uid='send_task_uid')
def send_task(sender, instance, **kwargs):
    """Update the data in Asana when creating or editing a task."""
    transaction.on_commit(lambda: tasks.send_task.delay(instance.id))
