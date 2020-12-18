from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase

from myrss.models.subscription import Subscription

def get_subscription_count_for(user):
    return len(Subscription.objects.subscriptions_for_user(user))

class NewSubscriptionViewTests(TestCase):
    def setUp(self):
        test_user = User.objects.get_or_create(username='testuser')
        self.client.force_login(test_user[0])
        self.user = User.objects.get(username='testuser')

    def test_invalid_link_does_not_add_feed(self):
        subscriptions_no_before = get_subscription_count_for(self.user)
        response = self.client.post(
                "/new_subscription", data={"link": "asdasd"}
        )
        subscriptions_no_after = get_subscription_count_for(self.user)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(subscriptions_no_before, subscriptions_no_after)

    def test_valid_link_but_invalid_rss_feed_is_not_added(self):
        subscriptions_no_before = get_subscription_count_for(self.user)

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/Google.html"}
        )
        subscriptions_no_after = get_subscription_count_for(self.user)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(subscriptions_no_before, subscriptions_no_after)


    def test_valid_rss_feed_is_correctly_added(self):
        subscriptions_no_before = get_subscription_count_for(self.user)

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        subs_after = Subscription.objects.subscriptions_for_user(self.user)
        subscriptions_no_after = len(subs_after)

        self.assertEqual("Clarin.com - Home", subs_after[len(subs_after)-1].name)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subscriptions_no_before+1, subscriptions_no_after)

    def test_another_valid_rss_feed_is_correctly_added(self):
        subscriptions_no_before = get_subscription_count_for(self.user)

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/pagina12rss.xml"}
        )
        my_subs = Subscription.objects.subscriptions_for_user(self.user)
        subscriptions_no_after = len(my_subs)
        self.assertEqual("El país | Página12", my_subs[subscriptions_no_before].name)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subscriptions_no_before+1, subscriptions_no_after)

    # an user cannot add a rss feed if already present in his feed
    def test_cannot_add_duplicate_feed(self):
        subs_init = get_subscription_count_for(self.user)
        self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/pagina12rss.xml"}
        )
        subscriptions_no_before = get_subscription_count_for(self.user)

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/pagina12rss.xml"}
        )
        my_subs = Subscription.objects.subscriptions_for_user(self.user)
        subscriptions_no_after = get_subscription_count_for(self.user)

        self.assertEqual("El país | Página12", my_subs[subs_init].name)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(subscriptions_no_before, subscriptions_no_after)

    def test_can_add_feed_even_if_present_in_another_users_feed(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )

        another_test_user = User.objects.get_or_create(username='testuser2')
        self.client.force_login(another_test_user[0])
        self.user = User.objects.get(username='testuser2')
        subscriptions_no_before = get_subscription_count_for(self.user)
        another_user_subscriptions = Subscription.objects.subscriptions_for_user(self.user)
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        subscriptions_no_after = get_subscription_count_for(self.user)

        self.assertEqual("Clarin.com - Home", another_user_subscriptions[subscriptions_no_after- 1].name)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subscriptions_no_before + 1, subscriptions_no_after)

    def test_adding_feed_does_not_modify_other_users_feed(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/pagina12rss.xml"}
        )
        subscriptions_no_before = get_subscription_count_for(self.user)
        subscriptions_before = Subscription.objects.subscriptions_for_user(self.user)

        another_test_user = User.objects.get_or_create(username='testuser2')
        self.client.force_login(another_test_user[0])
        self.user = User.objects.get(username='testuser2')

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )

        subscriptions_no_after = get_subscription_count_for(User.objects.get(username='testuser'))

        self.assertEqual("El país | Página12", subscriptions_before[subscriptions_no_after- 1].name)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subscriptions_no_before , subscriptions_no_after)


