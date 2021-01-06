from django.db import models

class FolderSubscription(models.Model):
    folder = models.ForeignKey('myrss.Folder', on_delete=models.CASCADE)
    subscription = models.ForeignKey('myrss.Subscription', on_delete=models.CASCADE)