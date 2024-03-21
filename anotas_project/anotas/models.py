from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
class Note(models.Model):
    noteTitle = models.CharField(max_length=128)
    noteID = models.AutoField(primary_key=True)
    #content = MarkdownxField(default="")
   # userID = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model
    #pastOwners = models.ManyToManyField(User, related_name='past_owners', blank=True)
    lastSave = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    isPrivate = models.BooleanField(default=False)
  #  viewCount = models.PositiveIntegerField(default=0)
   # copyCount = models.PositiveIntegerField(default=0)
    fileName = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.noteTitle