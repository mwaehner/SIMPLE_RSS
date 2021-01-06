from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateTimeField



class Folder(models.Model):
    subscriptions = models.ManyToManyField('myrss.Subscription', through='myrss.FolderSubscription')
    name = models.URLField(unique=True)

    def __str__(self):
        return self.name

