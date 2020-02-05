from django.contrib import admin
from core.models import File, Folder
from core.models import UserProfessor, UserCandidate



# Register your models here.
admin.site.register(File)
admin.site.register(Folder)
admin.site.register(UserProfessor)
admin.site.register(UserCandidate)
