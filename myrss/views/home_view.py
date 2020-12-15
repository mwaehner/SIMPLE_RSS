from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from myrss.models.subscription_form import SubscriptionForm
from myrss.models.subscription_model import Subscription


class HomeView(View):
    @method_decorator(login_required)
    def get(self, request):
        my_subs = Subscription.objects.subs_for_user(request.user)
        form = SubscriptionForm()
        return render(request, 'appUser/home.html', {'form': form, 'subs': my_subs})