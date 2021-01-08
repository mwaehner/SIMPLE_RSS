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
        try:
            news_feed = feedparser.parse(url)
        except:
            return 0
        added_article_count = 0
        #more recent news are at the beginning, we traverse in reversed order so that older articles are created in the DB first
        for entry in reversed(news_feed.entries):
            new_links = entry.get('links')
            imglink = ""
            if new_links:
                for new_link in new_links:
                    if re.match('image', new_link.get('type')):
                        imglink = new_link.get('href')
            (article, was_created) = Article.objects.get_or_create(
                link=entry.get('link'),
            )
            if not self.article_set.filter(link=article.link).exists():
                added_article_count += 1
            article.title = entry.get('title')
            article.summary = entry.get('summary')
            article.img_link = imglink
            article.save()
            article.subscriptions.add(self)
        return added_article_count

    class Meta:
        unique_together = ('link', 'owner',)



