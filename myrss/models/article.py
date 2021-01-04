from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateTimeField



class Article(models.Model):
    subscriptions = models.ManyToManyField('myrss.Subscription', through='SubscriptionArticle')
    link = models.URLField(unique=True)
    img_link = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=500)
    summary = models.CharField(max_length=1000, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

    def __str__(self):
        return self.title

class SubscriptionArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    subscription= models.ForeignKey('myrss.Subscription', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)