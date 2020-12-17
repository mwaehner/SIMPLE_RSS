from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import PermissionDenied
from http import HTTPStatus
import feedparser

from myrss.forms.subscription_form import SubscriptionForm
from myrss.models.article import Article
from myrss.models.subscription import Subscription



class ShowArticlesView(View):
    @method_decorator(login_required)
    def get(self, request, subscription_id):
        subscription = Subscription.objects.get(id=subscription_id)
        if not request.user == subscription.owner:
            raise PermissionDenied
        articles = subscription.article_set.all()
        k = len(articles)
        print(articles)
        last_articles = [articles[i] for i in range(min(10, len(articles)))]
        return render(request, 'user/showarticles.html', {'articles': last_articles})

