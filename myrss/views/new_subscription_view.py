from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from http import HTTPStatus

from myrss.forms.subscription_form import SubscriptionForm
from myrss.models.subscription import Subscription


class NewSubscriptionView(View):
    @method_decorator(login_required)
    def post(self, request):
        subscription = Subscription(owner=self.request.user)
        subscription_form = SubscriptionForm(instance=subscription, data=self.request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            return redirect('user_home')
        subscriptions = Subscription.objects.subscriptions_for_user(request.user)
        return render(request, 'user/home.html', {'subscription_form': subscription_form, 'subscriptions': subscriptions}, status=HTTPStatus.BAD_REQUEST)













