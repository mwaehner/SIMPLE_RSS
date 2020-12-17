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
        subs = Subscription(owner=self.request.user)
        subscription_form = SubscriptionForm(instance=subs, data=self.request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            return redirect('user_home')
        else:
            my_subs = Subscription.objects.subscriptions_for_user(request.user)
            return render(request, 'user/home.html', {'subscription_form': subscription_form, 'subs': my_subs}, status=HTTPStatus.BAD_REQUEST)













