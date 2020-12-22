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
        new_subscription_form = SubscriptionForm(instance=new_subscription, data=self.request.POST)
        if new_subscription_form.is_valid():
            new_subscription = new_subscription_form.save()
            new_subscription._add_articles_of_subscription()
            return redirect('user_home')

        user_subscriptions = Subscription.objects.subscriptions_for_user(request.user)
        return render(request, 'user/home.html', {'subscription_form': new_subscription_form, 'subscriptions': user_subscriptions}, status=HTTPStatus.BAD_REQUEST)














