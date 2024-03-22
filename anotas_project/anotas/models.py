from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from django.utils import timezone as tz
from django.contrib.postgres.fields import ArrayField

class Subject(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
class Note(models.Model):
    noteID = models.AutoField(primary_key=True)
    content = MarkdownxField(default="")
    userID = models.CharField(max_length=255, blank=True, null=True)
    #pastOwners = models.ManyToManyField(User, related_name='past_owners', blank=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    isPrivate = models.BooleanField(default=False)
    viewCount = models.PositiveIntegerField(default=0)
    copyCount = models.PositiveIntegerField(default=0)
    fileName = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True)
    
    def set_noteID(self, inp):
        self.noteID = inp
        
    def set_fileName(self):
        self.fileName = self.noteTitle + str(self.noteID) + ".md"
        
    def get_fileName(self):
        return self.fileName
        
    def set_userID(self, request):
        self.userID = request.user.get_username()
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.noteTitle)
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.noteTitle