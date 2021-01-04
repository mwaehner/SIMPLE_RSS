from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from http import HTTPStatus
from myrss.forms.subscription_form import SubscriptionForm
from myrss.models.article import Article
from myrss.models.subscription import Subscription


class DeleteSubscriptionView(View):
    @method_decorator(login_required)
    def post(self, request, subscription_id):
        subscription = Subscription.objects.get(pk=subscription_id)
        for article in subscription.article_set.all():
            if len(article.subscriptions.all()) == 1:
                article.delete()
        subscription.delete()
        return redirect('user_home')
