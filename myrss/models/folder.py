from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateTimeField

from myrss.models.folder_subscription import FolderSubscription


class Folder(models.Model):
    owner = models.ForeignKey(User, related_name="folder_owner", on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField('myrss.Subscription', through=FolderSubscription)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'owner',)

