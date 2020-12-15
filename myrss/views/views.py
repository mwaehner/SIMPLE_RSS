from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator

from myrss.models.forms import SubscriptionForm
from myrss.models.models import Subscription


class NewSubscription(View):
    @method_decorator(login_required)
    def post(self, request):
        subs = Subscription(from_user=self.request.user)
        form = SubscriptionForm(instance=subs, data=self.request.POST)
        if form.is_valid():
            form.save()
        return redirect('user_home')



class Welcome(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('user_home')
        else:
            return render(request, 'myrss/welcome.html')


class Home(View):
    @method_decorator(login_required)
    def get(self, request):
        my_subs = Subscription.objects.subs_for_user(request.user)
        form = SubscriptionForm()
        return render(request, 'appUser/home.html', {'form': form, 'subs': my_subs})



class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "appUser/signup_form.html"
    success_url = reverse_lazy('user_home')
