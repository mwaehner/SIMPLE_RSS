from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from myrss.models.subscription_article import SubscriptionArticle


class SetRead(View):
    @method_decorator(login_required)
    @csrf_exempt
    def post(self, request, article_id):
        subscription_article = SubscriptionArticle.objects.filter(subscription__owner=self.request.user, article=article_id)
        if subscription_article.exists():
            subscription_article_to_toggle = subscription_article.get()
            subscription_article_to_toggle.read = True
            subscription_article_to_toggle.save()
            data = {'success': 'set as read'}
            status_code = status.HTTP_200_OK
        else:
            data = {'failure': 'article does not exist'}
            status_code = status.HTTP_400_BAD_REQUEST
        return JsonResponse(data, status=status_code)
