from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateTimeField



class Article(models.Model):
    subscriptions = models.ManyToManyField('myrss.Subscription', through='myrss.SubscriptionArticle')
    link = models.URLField(unique=True)
    img_link = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=500)
    summary = models.CharField(max_length=1000, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

    def __str__(self):
        return self.title

