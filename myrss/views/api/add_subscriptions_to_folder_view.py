

from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
from django.db import *
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.utils import json
from django.db.models import Q
from myrss.models.folder import Folder
from myrss.models.folder_subscription import FolderSubscription
from myrss.models.subscription import Subscription
from myrss.models.subscription_article import SubscriptionArticle


class AddSubscriptionsToFolder(View):
    @method_decorator(login_required)
    @csrf_exempt
    def post(self, request):
        data = request.POST
        folder_id = data['folderId']
        subscriptions_data = data['subscriptionIds']
        subscription_ids = json.loads(subscriptions_data)
        try:
            folder = Folder.objects.get(owner=self.request.user, pk=folder_id)
        except Folder.DoesNotExist:
            data = {'failure': 'folder does not exist'}
            status_code = status.HTTP_400_BAD_REQUEST
            return JsonResponse(data, status=status_code)
        subscriptions_of_other_users = Subscription.objects.filter(~Q(owner=self.request.user), id__in=subscription_ids)
        if subscriptions_of_other_users.exists():
            data = {'failure': 'subscription does not exist'}
            status_code = status.HTTP_400_BAD_REQUEST
            return JsonResponse(data, status=status_code)
        for subscription_id in subscription_ids:
            try:
                FolderSubscription.objects.get_or_create(folder_id=folder_id, subscription_id=subscription_id)
            except IntegrityError:
                data = {'failure': 'subscription does not exist'}
                status_code = status.HTTP_400_BAD_REQUEST
                return JsonResponse(data, status=status_code)
        data = {'success': 'added subscriptions to folder'}
        status_code = status.HTTP_200_OK
        return JsonResponse(data, status=status_code)