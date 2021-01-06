from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from http import HTTPStatus
import feedparser
import re

from myrss.forms.subscription_form import SubscriptionForm
from myrss.forms.folder_form import FolderForm

from myrss.models.folder import Folder
from myrss.models.subscription import Subscription


class NewFolderView(View):
    @method_decorator(login_required)
    def post(self, request):
        new_folder = Folder(owner=self.request.user)
        new_folder_form = FolderForm(instance=new_folder, data=self.request.POST)
        if new_folder_form.is_valid():
            new_folder = new_folder_form.save()
            return redirect('user_home')

        user_subscriptions = Subscription.objects.subscriptions_for_user(request.user)
        folders = Folder.objects.filter(owner=request.user)
        return render(request, 'user/home.html', {'subscription_form': SubscriptionForm(), 'folder_form': new_folder_form, 'subscriptions': user_subscriptions,
                                                  'folders': folders}, status=HTTPStatus.BAD_REQUEST)