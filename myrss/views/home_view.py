from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from myrss.forms.folder_form import FolderForm
from myrss.forms.subscription_form import SubscriptionForm
from myrss.models.folder import Folder
from myrss.models.subscription import Subscription



class HomeView(View):
    @method_decorator(login_required)
    def get(self, request):
        user_subscriptions = Subscription.objects.subscriptions_for_user(request.user)
        folders = Folder.objects.filter(owner=request.user)
        return render(request, 'user/home.html', {'subscription_form': SubscriptionForm(), 'folder_form': FolderForm(),
                                                  'subscriptions': user_subscriptions, 'folders': folders})
