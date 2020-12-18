from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from http import HTTPStatus
import feedparser
import re

from myrss.forms.subscription_form import SubscriptionForm
from myrss.models.article import Article
from myrss.models.subscription import Subscription


class NewSubscriptionView(View):
    @method_decorator(login_required)
    def post(self, request):
        new_subscription = Subscription(owner=self.request.user)
        form = SubscriptionForm(instance=new_subscription, data=self.request.POST)
        if form.is_valid():
            new_subscription = form.save()
            url = new_subscription.link
            news_feed = feedparser.parse(url)
            for i in range(len(news_feed.entries)):
                newlink = news_feed.entries[i].get('link')
                newtitle = news_feed.entries[i].get('title')
                newsummary = news_feed.entries[i].get('summary')
                newlinks = news_feed.entries[i].get('links')
                imglink = ""
                for j in range(len(newlinks)):
                    if newlinks!= None and len(newlinks)>0 and re.match('image', newlinks[j].get('type')):
                        imglink = newlinks[j].get('href')
                (article, was_created) = Article.objects.get_or_create(
                    link = news_feed.entries[i].get('link'),
                    title = news_feed.entries[i].get('title'),
                    summary = news_feed.entries[i].get('summary'),
                    img_link = imglink
                )
                article.subscriptions.add(new_subscription)


        else:
            my_subs = Subscription.objects.subscriptions_for_user(request.user)
            return render(request, 'user/home.html', {'form': form, 'subs': my_subs}, status=HTTPStatus.BAD_REQUEST)
        return redirect('user_home')












