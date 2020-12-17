from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from myrss.forms.subscription_form import SubscriptionForm
from myrss.models.subscription import Subscription


class NewSubscriptionView(View):
    @method_decorator(login_required)
    def post(self, request):
        subs = Subscription(owner=self.request.user)
        form = SubscriptionForm(instance=subs, data=self.request.POST)
        if form.is_valid():
            form.save()
        else:
            my_subs = Subscription.objects.subscriptions_for_user(request.user)
            return render(request, 'user/home.html', {'form': form, 'subs': my_subs})
        return redirect('user_home')












