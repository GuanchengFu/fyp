from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import File, Folder
from core.models import UserProfessor, UserCandidate, User



# Register your models here.
admin.site.register(File)
admin.site.register(Folder)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfessor)
admin.site.register(UserCandidate)
