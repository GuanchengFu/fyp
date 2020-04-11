from django.dispatch import receiver
from django.db import models
from django.dispatch import Signal
from core.models import File, notify_handler, Message, RelationshipRequest
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
    'timestamp', 'button_class',
])

# connect the signal
notify.connect(notify_handler, dispatch_uid='core.notifications')


@receiver(models.signals.post_save, sender=Message)
def notify_new_message(sender, instance, created, **kwargs):
    """
    Username has sent you a message.
    Username: actor
    verb: has sent
    action_object: you
    target: A message.
    time: The time since.
    """
    if created:
        notify.send(sender, actor=instance.sender, verb='has sent you a', recipient=[instance.receiver],
                    action_object=instance, button_class='message', )


@receiver(models.signals.post_save, sender=RelationshipRequest)
def notify_new_relationship(sender, instance, created, **kwargs):
    """
    Username has sent you a request.
    """
    if created:
        notify.send(sender, actor=instance.sender, verb='has sent you a', recipient=[instance.recipient],
                    action_object=instance, button_class='relationship_request',)

