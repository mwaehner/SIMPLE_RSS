from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from http import HTTPStatus
from myrss.forms.subscription_form import SubscriptionForm
from myrss.models.article import Article
from myrss.models.subscription import Subscription


class UpdateSubscriptionView(View):
    @method_decorator(login_required)
    def post(self, request, subscription_id):
        subscription = Subscription.objects.get(pk=subscription_id)
        if not request.user == subscription.owner:
            raise PermissionDenied
        new_articles_added = subscription.get_last_articles()
        user_subscriptions = Subscription.objects.subscriptions_for_user(request.user)
        return render(request, 'user/home.html',
                      {'subscription_form': SubscriptionForm(), 'subscriptions': user_subscriptions, 'show_updated': True, 'updated_no': new_articles_added})

