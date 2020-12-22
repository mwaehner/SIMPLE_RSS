from django.contrib.auth.models import User
from django.db import models
from myrss.models.subscription import Subscription


class Article(models.Model):
    subscriptions = models.ManyToManyField(Subscription)
    link = models.URLField(unique=True)
    img_link = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=500)
    summary = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.title