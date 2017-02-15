from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Notefile(models.Model):
    author = models.ForeignKey('auth.User')
    name = models.CharField(max_length=200)
    label = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)

    class Meta:
        unique_together = ('author', 'name',)

    def create(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

class Notecard(models.Model):
    author = models.ForeignKey('auth.User')
    name = models.CharField(max_length=200)
    label = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    notefile = models.ForeignKey(Notefile, on_delete=models.CASCADE)

    def create(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

class Directories(models.Model):
    author = models.ForeignKey('auth.User')
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(
            default=timezone.now)
    parent_directory = models.ForeignKey('self',related_name='child_directory', null=True, on_delete=models.CASCADE)

    def create(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name
