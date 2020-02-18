from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import File, Folder
from core.models import UserProfessor, UserCandidate, User

class ProfessorAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Register your models here.
admin.site.register(File)
admin.site.register(Folder)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfessor, ProfessorAdmin)
admin.site.register(UserCandidate)
