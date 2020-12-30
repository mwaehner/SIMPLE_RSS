from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import PermissionDenied
from http import HTTPStatus
import feedparser

from myrss.forms.subscription_form import SubscriptionForm
from myrss.models.article import Article, SubscriptionArticle
from myrss.models.subscription import Subscription



class ShowArticlesView(View):
    @method_decorator(login_required)
    def get(self, request, subscription_id):
        subscription = Subscription.objects.get(id=subscription_id)
        if not request.user == subscription.owner:
            raise PermissionDenied
        articles = subscription.article_set.all()
        articles_no = min(10, len(articles))
        last_articles_content = [articles[len(articles)-i-1] for i in range(articles_no)]
        last_articles_readStatus = [SubscriptionArticle.objects.get(article=last_articles_content[i].id, subscription=subscription_id).read for i in range(articles_no)]
        last_articles = zip(last_articles_content, last_articles_readStatus)

        return render(request, 'user/show_articles.html', {'articles': last_articles, })

