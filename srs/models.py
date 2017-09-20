from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import User

def create_folder(sender, instance, created, **kwargs):
    if not created:  # if it's not a new object return
        return

    home_directory = Directory()
    home_directory.author = instance
    home_directory.name = 'Home'
    home_directory.save()

post_save.connect(create_folder, sender=User)

class Directory(models.Model):
    author = models.ForeignKey('auth.User')
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(
            default=timezone.now)
    parent_directory = models.ForeignKey('self',related_name='child_directory', null=True, on_delete=models.CASCADE)

    def create(self) -> object:
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

class Notefile(models.Model):
    author = models.ForeignKey('auth.User')
    name = models.CharField(max_length=200)
    keywords = models.TextField(null=True)
    label = models.TextField(null=True)
    body = models.TextField(null=True)
    created_date = models.DateTimeField(
            default=timezone.now)
    directory = models.ForeignKey(Directory, null=True, on_delete=models.CASCADE)

    def create(self):
        self.created_date = timezone.now()
        #Define default directory to Home
        if self.directory is None:
            self.directory = Directory.objects.filter(name='Home').values('id')
        self.save()

    def __str__(self):
        return self.name

        return 

class Notecard(models.Model):
    author = models.ForeignKey('auth.User')
    name = models.CharField(max_length=200)
    keywords = models.TextField(null=True)
    label = models.TextField(null=True)
    body = models.TextField(null=True)
    created_date = models.DateTimeField(
            default=timezone.now)
    notefile = models.ForeignKey(Notefile, on_delete=models.CASCADE)

    def create(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

class Video(models.Model):
    author = models.ForeignKey('auth.User')
    url = models.CharField(max_length=200)
    notecard = models.ForeignKey(Notecard, null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(
            default=timezone.now)

    def create(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.url
