from django.apps import AppConfig


class AsanaCrmConfig(AppConfig):
    name = 'asana_crm'

    # noinspection PyUnresolvedReferences
    def ready(self):
        import asana_crm.signals
