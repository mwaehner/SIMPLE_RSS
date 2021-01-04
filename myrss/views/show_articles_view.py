from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import PermissionDenied
from http import HTTPStatus
import feedparser

from myrss.forms.subscription_form import SubscriptionForm
from myrss.models.article import Article
from myrss.models.subscription_article import SubscriptionArticle
from myrss.models.subscription import Subscription



class ShowArticlesView(View):
    @method_decorator(login_required)
    def get(self, request, subscription_id):
        articles_number_to_show = 10
        last_articles = SubscriptionArticle.objects.filter(subscription=subscription_id).order_by('-article__created_at').all()[:articles_number_to_show]
        return render(request, 'user/show_articles.html', {'subscription_articles': last_articles})

