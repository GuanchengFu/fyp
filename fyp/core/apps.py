from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    This class is used to handle the import conflicts
    """
    name = 'core'

    def ready(self):
        import core.signals
        from core.signals import notify
