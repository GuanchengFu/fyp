from django.dispatch import receiver
from django.db import models
from django.dispatch import Signal
from core.models import File
import os


@receiver(models.signals.post_delete, sender=File)
def auto_delete_files_on_file_object(sender, instance, **kwargs):
    """
    When the File object is deleted, this method will be called.
    reference:
    https://stackoverflow.com/questions/16041232/django-delete-filefield
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


# A customizing signal.
notify = Signal(providing_args=[  # pylint: disable=invalid-name
    'recipient', 'actor', 'verb', 'action_object', 'target', 'description',
    'timestamp', 'level'
])