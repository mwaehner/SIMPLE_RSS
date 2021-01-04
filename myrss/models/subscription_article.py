from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateTimeField
from myrss.models.article import Article

class SubscriptionArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    subscription= models.ForeignKey('myrss.Subscription', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)