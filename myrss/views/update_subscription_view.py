from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from http import HTTPStatus

from myrss.forms.folder_form import FolderForm
from myrss.forms.subscription_form import SubscriptionForm
from myrss.models.article import Article
from myrss.models.folder import Folder
from myrss.models.subscription import Subscription


class UpdateSubscriptionView(View):
    @method_decorator(login_required)
    def post(self, request, subscription_id):
        subscription = Subscription.objects.get(pk=subscription_id, owner=request.user)
        new_articles_added = subscription.get_last_articles()
        user_subscriptions = Subscription.objects.subscriptions_for_user(request.user)
        folders = Folder.objects.filter(owner=request.user)
        return render(request, 'user/home.html',
                      {'subscription_form': SubscriptionForm(), 'folder_form': FolderForm(), 'subscriptions': user_subscriptions,
                                                  'folders': folders, 'show_updated': True, 'updated_count': new_articles_added})

