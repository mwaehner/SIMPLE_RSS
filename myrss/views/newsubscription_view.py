from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from myrss.models.subscription_form import SubscriptionForm
from myrss.models.subscription_model import Subscription
import feedparser

class NewSubscriptionView(View):
    @method_decorator(login_required)
    def post(self, request):
        subs = Subscription(from_user=self.request.user)
        form = SubscriptionForm(instance=subs, data=self.request.POST)
        if form.is_valid():
            form.save()
        else:
            my_subs = Subscription.objects.subs_for_user(request.user)
            return render(request, 'user/home.html', {'form': form, 'subs': my_subs})
        return redirect('user_home')












