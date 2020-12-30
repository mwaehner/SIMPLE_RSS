from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase

from myrss.models.article import Article
from myrss.models.subscription import Subscription

def get_subscription_count_for(user):
    return len(Subscription.objects.subscriptions_for_user(user))

class DeleteSubscriptionViewTests(TestCase):
    def setUp(self):
        test_user = User.objects.get_or_create(username='testuser')
        self.client.force_login(test_user[0])
        self.user = User.objects.get(username='testuser')


    def test_subscription_no_decreases_when_deleting_subscription(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        subscriptions_no_before = get_subscription_count_for(self.user)
        subscription_id = Subscription.objects.get(owner=self.user).id

        response = self.client.post(
            "/delete_subscription/" + str(subscription_id) + '/', follow=True, data={}
        )
        subscriptions_no_after = get_subscription_count_for(self.user)
        self.assertEqual(subscriptions_no_after+1, subscriptions_no_before)

    def test_deleting_subscription_from_user_does_not_delete_other_users_subscriptions(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        subscriptions_no_before = get_subscription_count_for(self.user)
        another_test_user = User.objects.get_or_create(username='testuser2')
        self.client.force_login(another_test_user[0])
        self.user = User.objects.get(username='testuser2')
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )

        subscription_id = Subscription.objects.get(owner=self.user).id
        response = self.client.post(
            "/delete_subscription/" + str(subscription_id) + '/', follow=True, data={}
        )

        subscriptions_no_after = get_subscription_count_for(User.objects.get(username='testuser'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subscriptions_no_before, subscriptions_no_after)
