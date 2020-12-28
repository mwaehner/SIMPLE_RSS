from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from http import HTTPStatus
from myrss.models.article import SubscriptionArticle


class ChangeReadStatusView(View):
    @method_decorator(login_required)
    def get(self, request, subscription_id, article_id):
        subscription_article = SubscriptionArticle.objects.get(subscription=subscription_id, article=article_id)
        subscription_article.read = True
        subscription_article.save()
        return HTTPStatus.OK

