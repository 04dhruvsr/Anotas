from django.contrib import admin
from django.contrib.auth.models import User

from django.contrib import admin
from anotas.models import Subject, Page, Note, UserProfile

class SubjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Subject, SubjectAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(Note)