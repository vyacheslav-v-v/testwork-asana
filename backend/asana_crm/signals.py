from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from asana_crm import tasks
from asana_crm.models import Project, Task

# Здесь не хватает синхронизации проектов при изменении состава проектов у
# задачи или состава задач программно без пересохранения задачи.
# Чтобы это обработать необходимо перехватывать сигнал m2m_changed от sender-а
# Task.projects.through.

# Желательно также предусмотреть случаи, когда происходит пересохранение
# объекта без его фактического изменения. В этом случае синхронизацию делать не
# нужно.
# Но для этого надо также учитывать, что при пересохранении может вызываться
# метод Task.projects.set() или Project.tasks.set() вызывает сигналы с
# action-ами pre_clear и post_add
# Можно в action-ах pre_clear сохранять список текущих проектов у задачи,
# или список задач у проекта в instance и затем, при получении сигнала с
# action-м post_add, сравнивать старый и новый списки чтобы определить
# изменилось ли что-либо.

@receiver(post_save, sender=Project, dispatch_uid='send_project_uid')
def send_project(sender, instance, **kwargs):
    """ При создании или редактировании проекта обновляем данные в Asana. """
    # Мы ещё находимся в незавершённой транзакции. Поэтому, если мы задачу
    # создадим напрямую, воркер её может подхватить раньше, чем произойдёт
    # коммит. В этом случае мы можем отправить в Asana не актуальные данные,
    # либо, если это новый проект, таска его может не найти вовсе.
    # Чтобы это исключить используем on_commit.
    transaction.on_commit(lambda: tasks.send_project.delay(instance.id))


@receiver(post_save, sender=Task, dispatch_uid='send_task_uid')
def send_task(sender, instance, **kwargs):
    """ При создании или редактировании задачи обновляем данные в Asana. """
    transaction.on_commit(lambda: tasks.send_task.delay(instance.id))
