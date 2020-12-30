from django.contrib.auth.models import User
from django.db import models
import feedparser
import re
from myrss.models.article import Article


class SubscriptionQuerySet(models.QuerySet):
    def subscriptions_for_user(self, user):
        return self.filter(
            owner=user
        )


class Subscription(models.Model):
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    link = models.CharField(max_length=300)
    name = models.CharField(max_length=350)
    objects = SubscriptionQuerySet.as_manager()

    def __str__(self):
        return self.name

    def get_last_articles(self):
        url = self.link
        news_feed = feedparser.parse(url)
        added_no = 0
        #we traverse the news in reversed order to add the most recent news at the last rows
        for i in range(len(news_feed.entries)-1,-1,-1):
            newlinks = news_feed.entries[i].get('links')
            imglink = ""
            for j in range(len(newlinks)):
                if newlinks != None and len(newlinks) > 0 and re.match('image', newlinks[j].get('type')):
                    imglink = newlinks[j].get('href')
            (article, was_created) = Article.objects.get_or_create(
                link=news_feed.entries[i].get('link'),
            )
            if not self.article_set.filter(link=article.link).exists():
                added_no+=1
            article.title = news_feed.entries[i].get('title')
            article.summary = news_feed.entries[i].get('summary')
            article.img_link = imglink
            article.save()
            article.subscriptions.add(self)
        return added_no

    class Meta:
        unique_together = ('link', 'owner',)



