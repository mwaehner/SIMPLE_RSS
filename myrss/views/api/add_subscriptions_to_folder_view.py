

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.utils import json

from myrss.models.folder import Folder
from myrss.models.subscription import Subscription
from myrss.models.subscription_article import SubscriptionArticle


class AddSubscriptionsToFolder(View):
    @method_decorator(login_required)
    @csrf_exempt
    def post(self, request):
        data = request.POST
        folder_name = data['folder']
        subscriptions = data['subscriptions']
        subscription_ids = json.loads(subscriptions)['selectedSubscriptions']
        try:
            folder = Folder.objects.get(name=folder_name)
        except:
            data = {'failure': 'folder does not exist'}
            status_code = status.HTTP_400_BAD_REQUEST
            return JsonResponse(data, status=status_code)
        for subscription_id in subscription_ids:
            try:
                subscription = Subscription.objects.get(id=subscription_id)
            except:
                data = {'failure': 'subscription does not exist'}
                status_code = status.HTTP_400_BAD_REQUEST
                return JsonResponse(data, status=status_code)
            folder.subscriptions.add(subscription)
        data = {'success': 'toggled read'}
        status_code = status.HTTP_200_OK
        return JsonResponse(data, status=status_code)