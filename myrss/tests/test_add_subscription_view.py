from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase

from myrss.models.subscription_model import Subscription


class AddSubscriptionFormTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        self.user = User.objects.get(username='testuser')
    def test_adding_sub_ok(self):
        my_subs = Subscription.objects.subs_for_user(self.user)
        print(len(my_subs))
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "https://www.clarin.com/rss/politica/"}
        )
        my_subs = Subscription.objects.subs_for_user(self.user)
        print(len(my_subs))
        self.assertEqual(response.status_code, HTTPStatus.OK)