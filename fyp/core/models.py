from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
#Later on, change the store position of the files so that it looks the same as the way user stores it.

#Further improvement may be found at:
#https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/#upload-handlers


"""
One folder may belongs to:
1. A specific user.
2. Another folder.
"""

#底层考虑直接将所有文件存在一个地址，实时的根据用户的选项来构建视图（view）
#This may be changed after.
def file_location_path(instance, filename):
	# file will be uploaded to "client_files/<id>/Y/m/d/<filename>"
	return 'client_files/{0}/{1}/{2}'.format(instance.user.id, datetime.datetime.now(datetime.timezone.utc).date().strftime("%Y/%m/%d"), filename)


""".
Possible reference for DateField:
https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add

There should not have two files with the same name in the folder.
"""


class File(models.Model):
	user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='userfiles')
	folder = models.ForeignKey('Folder', on_delete=models.CASCADE, related_name='files', null=True)
	description = models.CharField(max_length=70)
	file = models.FileField(upload_to='test/files/', null=False, blank=True)
	created = models.DateTimeField(editable=False, null=True)
	modified = models.DateTimeField(null=True)

	def save(self, *args, **kwargs):
		# if the object is newly created:
		if not self.id:
			self.created = timezone.now()
		self.modified = timezone.now()
		super().save(*args, **kwargs)

	class Meta:
		verbose_name_plural = "Files"

	def __str__(self):
		return self.description


"""
Folder is a model for the folders stored by the user.
The related name attribute is a reference hold by the foreign key to access all the folders
related to the user or the folder.
"""
class Folder(models.Model):
	# user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='userfolders')
	folder = models.ForeignKey('self', on_delete=models.CASCADE, related_name='folders', null=True)

	# The name may need to be checked to see whether the naming convention is complied.
	name = models.CharField(max_length=70)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Folders"


class User(AbstractUser):
	# assDefine the additional information.
	USERNAME_FIELD = 'email'
	email = models.EmailField(_('email address'), unique=True)
	REQUIRED_FIELDS = ['username', 'password']
	is_professor = models.BooleanField('professor status', default=False)
	is_candidate = models.BooleanField('candidate status', default=False)

	class Meta:
		unique_together = ('email',)





"""
A model which is used to model the professor."""




class UserProfessor(models.Model):

	# To get the UserProfessor, use the user.profile to get it.
	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='professor')

	# picture will be uploaded to MEDIA_ROOT/profile_images
	picture = models.ImageField(upload_to='professor_images', blank=True)

	def __str__(self):
		return self.user.username



"""The candidate account should only be active until the professor has verfied
their account."""
class UserCandidate(models.Model):

	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='candidate')

	professor = models.ForeignKey(UserProfessor, on_delete=models.CASCADE, related_name="students", null=False)

	picture = models.ImageField(upload_to='candidate_images', blank=True)

	def __str__(self):
		return self.user.username


