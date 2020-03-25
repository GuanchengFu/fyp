from datetime import datetime
import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.dispatch import receiver

# Later on, change the store position of the files so that it looks the same as the way user stores it.

# Further improvement may be found at:
# https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/#upload-handlers


"""
One folder may belongs to:
1. A specific user.
2. Another folder.
"""


# 底层考虑直接将所有文件存在一个地址，实时的根据用户的选项来构建视图（view）
# This may be changed after.
def file_location_path(instance, filename):
    # file will be uploaded to "client_files/<id>/Y/m/d/<filename>"
    return 'client_files/{0}/{1}'.format(instance.user.id, filename)


""".
Possible reference for DateField:
https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add

There should not have two files with the same name in the folder.
"""


class File(models.Model):
    """
    A model for the file uploaded by the user.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='userfiles')
    description = models.CharField(max_length=70, blank=True)
    file = models.FileField(upload_to=file_location_path, blank=False)
    name = models.CharField(max_length=70, blank=False)
    created = models.DateTimeField(editable=False, null=True)
    modified = models.DateTimeField(null=True)

    __original_name = None

    def __init__(self, *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)
        self.__original_name = self.name

    def save(self, *args, **kwargs):
        # if the object is newly created:
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super().save(*args, **kwargs)
        """
        The following operations are used to change the file name if the user change the 
        file name in the form.
        reference:
        https://stackoverflow.com/questions/1355150/when-saving-how-can-you-check-if-a-field-has-changed
        """
        if self.name != self.__original_name:
            """
            Need to handle the fileExistError.
            Two different cases:
            1. When the user upload the file.  Then make sure the file.name is the same as its name in the database.
            2. Change name to a already existed name.  Then maybe just abort this action.
            """
            new_path = os.path.join(os.path.dirname(self.file.path), self.name)
            try:
                os.rename(self.file.path, new_path)
            except FileExistsError:
                self.name = os.path.basename(self.file.path)
        super().save(*args, **kwargs)
        self.__original_name = self.name

    class Meta:
        verbose_name_plural = "Files"

    def __str__(self):
        return self.description


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


class UserManager(models.Manager):
    """
    A customizing manager class which is used to return some useful queryset.
    """
    def possible_recipients_for(self, user):
        """
        Return the user list whose can be the potential recipients of the
        message.
        possible_list = User.objects.possible_recipients_for(user)
        """
        if user.is_candidate:
            return self.filter(
                email=user.candidate.professor.user.email
            )
        if user.is_professor:
            return self.filter(
                is_candidate=True,
            )


class User(AbstractUser):
    """
    Customized user class.
    The email of each account should be unique.
    The user should use email and password to be authenticated.
    reference:
    https://stackoverflow.com/questions/37332190/django-login-with-email
    Unique attributes: username and email
    """
    # USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    # REQUIRED_FIELDS = ('username', 'password')
    is_professor = models.BooleanField('professor status', default=False)
    is_candidate = models.BooleanField('candidate status', default=False)

    def __str__(self):
        return self.username

    def is_candidate_of_professor(self, candidate_list):
        if self.is_professor:
            return False
        if self.is_candidate:
            if self.email in candidate_list:
                return True
        return False


class UserProfessor(models.Model):
    """
    A model for the professor user.
    Each professor should has a one-to-one relationship with a User object.
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='professor')
    collaborated_professors = models.ManyToManyField('self', related_name='collaborated_professors')
    # picture will be uploaded to MEDIA_ROOT/professor_images
    picture = models.ImageField(upload_to='professor_images', blank=True)

    def __str__(self):
        return self.user.username

    def candidates_email_set(self):
        result = []
        for c in self.students.all():
            result.append(c.user.email)
        return result


class UserCandidate(models.Model):
    """
    The candidate account should only be active until the professor has verified
    their account. -- Implemented later.
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='candidate')

    professor = models.ManyToManyField(UserProfessor, related_name='students')

    picture = models.ImageField(upload_to='candidate_images', blank=True)

    def __str__(self):
        return self.user.username


class MessageManager(models.Manager):
    """
    A customizing manager class which is used to return some useful queryset.
    """
    def inbox_for(self, user):
        """
        Return all messages that were received by the given user and are not marked as deleted.
        """
        return self.filter(
            receiver=user,
            is_receiver_delete=False,
        )

    def outbox_for(self, user):
        """
        Returns all the messages that were sent by the user and was not
        deleted by the user.
        """
        return self.filter(
            sender=user,
            is_sender_delete=False,
        )

    def trash_for(self, user):
        """
        Return all the messages that were either received or sent by the user
        and the user has deleted the message.
        """
        return self.filter(
            receiver=user,
            is_receiver_delete=True,
        ) | self.filter(
            sender=user,
            is_sender_delete=True,
        )


class Message(models.Model):
    """
    A message sent by a user to another user.
    The SET_NULL attribute will set the attribute to null, if the foreignkey is deleted.
    """
    subject = models.CharField(_("Subject"), max_length=70, blank=False)
    body = models.CharField(max_length=250, blank=True)

    sender = models.ForeignKey(get_user_model(), related_name="sent_messages", on_delete=models.PROTECT)
    receiver = models.ForeignKey(get_user_model(), related_name="received_messages", on_delete=models.SET_NULL,
                                 blank=True, null=True)
    # The user may want to send a reply to the sender.
    parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True,
                                   verbose_name="parent message", on_delete=models.SET_NULL)

    sent_at = models.DateTimeField(editable=False, blank=True, null=True)
    file = models.FileField(upload_to='temp_files', blank=True, null=True)

    is_read = models.BooleanField(blank=False, default=False)
    is_sender_delete = models.BooleanField(blank=False, default=False)
    is_receiver_delete = models.BooleanField(blank=False, default=False)

    objects = MessageManager()

    def save(self, *args, **kwargs):
        # if the object is newly created:
        if not self.id:
            self.sent_at = timezone.now()
        super(Message, self).save(*args, **kwargs)

    class Meta:
        ordering = ['sent_at']


class Group(models.Model):
    """
    A group created by one of the professor.
    The group can be used to send multiple messages.
    Send message to all the group members.

    creator: The creator of the group, only the creator can have the authority to delete the group.
    creator will be automatically be the manager of the group.

    All the professor can send group messages while the members can only receive group messages.

    member: The member can only be able to send personal message to their supervisor.
    """
    title = models.CharField(max_length=70, blank=False)
    creator = models.ForeignKey(UserProfessor, related_name="created_groups", on_delete=models.CASCADE)
    members = models.ManyToManyField(UserCandidate, related_name="participants")



