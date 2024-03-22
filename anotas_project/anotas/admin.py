from django.contrib import admin
from django.contrib.auth.models import User

from django.contrib import admin
from anotas.models import Subject, Note, UserProfile

class SubjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

    

    

    

admin.site.register(UserProfile)
