import factory

from asana_crm.models import Project, Workspace, AsanaUser, Task


class WorkspaceFactory(factory.DjangoModelFactory):
    name = factory.Faker('text', max_nb_chars=50)
    gid = factory.Faker('pystr', max_chars=5)

    # Костыль чтобы подсказать Pycharm-у тип создаваемого объекта.
    def __new__(cls, *args, **kwargs) -> Workspace:
        return super().__new__(*args, **kwargs)

    class Meta:
        model = Workspace


class ProjectNotSyncedFactory(factory.DjangoModelFactory):
    """ Фактори проектов, ранее не синхронизированных, с пустым gid. """
    name = factory.Faker('text', max_nb_chars=50)
    workspace = factory.Iterator(Workspace.objects.all())

    # Костыль чтобы подсказать Pycharm-у тип создаваемого объекта.
    def __new__(cls, *args, **kwargs) -> Project:
        return super().__new__(*args, **kwargs)

    class Meta:
        model = Project


class ProjectFactory(ProjectNotSyncedFactory):
    """ Фактори проектов. """
    gid = factory.Faker('pystr', max_chars=5)

    class Meta:
        model = Project


class TaskFactory(factory.DjangoModelFactory):
    """ Фактори задач. """
    name = factory.Faker('text', max_nb_chars=50)
    notes = factory.Faker('text', max_nb_chars=250)
    assignee = factory.Iterator(AsanaUser.objects.all())
    workspace = factory.Iterator(Workspace.objects.all())
    gid = factory.Faker('pystr', max_chars=5)

    @factory.post_generation
    def projects(self, create, projects):
        """Создаём один или несколько проектов, если они переданы в параметрах.

        Пример использования TaskFactory(projects=['Проект 1', 'Проект 2'])
        Принимает либо название проекта, либо список, состоящий либо из
        названий проектов, либо из проектов, либо из словаря для передачи в 
        ProjectFactory.
        """
        if not create:
            return
        if projects:
            result = []
            # если передано просто название одной группы
            if isinstance(projects, str):
                result.append(ProjectFactory(name=projects))
            else:
                for g in projects:
                    if isinstance(g, Project):
                        result.append(g)
                    elif isinstance(g, str):
                        result.append(ProjectFactory(name=g))
                    else:
                        result.append(ProjectFactory(**g))
            self.projects.add(*result)

    # Костыль чтобы подсказать Pycharm-у тип создаваемого объекта. 
    def __new__(cls, *args, **kwargs) -> Task:
        return super().__new__(*args, **kwargs)
    
    class Meta:
        model = Task
