from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from django.utils import timezone as tz
from django.contrib.postgres.fields import ArrayField

class Subject(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Page(models.Model):
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    #this comes from rango implementation might delete
    website = models.URLField(blank=True) 
    picture = models.ImageField(upload_to='profile_images', blank=True) 

    def __str__(self):
        return self.user.username
    
class Note(models.Model):
    noteID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(UserProfile, on_delete=models.CASCADE) 
    noteTitle = models.CharField(max_length=128)
    past_owners = models.CharField(max_length = 255, blank=True)
    lastSave = models.DateTimeField(default = tz.now) #auto_now=True
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # content = MarkdownxField(default="")   #do we need this?
    isPrivate = models.BooleanField(default=False)
    viewCount = models.PositiveIntegerField(default=0)
    copyCount = models.PositiveIntegerField(default=0)
    fileName = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.noteTitle
