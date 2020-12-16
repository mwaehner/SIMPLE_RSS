from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase

from myrss.models.subscription_model import Subscription


class AddSubscriptionViewTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser2')[0])
        self.user = User.objects.get(username='testuser2')

    def test_invalid_link_does_not_add_feed(self):
        my_subs = Subscription.objects.subs_for_user(self.user)
        subsno = len(my_subs)
        response = self.client.post(
                "/new_subscription", data={"link": "asdasd"}
        )
        my_subs = Subscription.objects.subs_for_user(self.user)
        afteradding_subsno = len(my_subs)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subsno, afteradding_subsno)

    #valid link but invalid rss
    def test_invalid_rss_feed_is_not_added(self):
        my_subs = Subscription.objects.subs_for_user(self.user)
        subsno = len(my_subs)

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/Google.html"}
        )
        my_subs = Subscription.objects.subs_for_user(self.user)
        afteradding_subsno = len(my_subs)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subsno, afteradding_subsno)


    def test_valid_rss_feed_is_correctly_added(self):
        subs_before = Subscription.objects.subs_for_user(self.user)
        len_before = len(subs_before)

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        subs_after = Subscription.objects.subs_for_user(self.user)
        len_after = len(subs_after)

        self.assertEqual("Clarin.com - Home", subs_after[len(subs_after)-1].name)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len_before+1, len_after)

    def test_another_valid_rss_feed_is_correctly_added(self):
        my_subs = Subscription.objects.subs_for_user(self.user)
        subsno = len(my_subs)

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/pagina12rss.xml"}
        )
        my_subs = Subscription.objects.subs_for_user(self.user)
        afteradding_subsno = len(my_subs)
        self.assertEqual("El país | Página12", my_subs[subsno].name)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subsno+1, afteradding_subsno)

    def test_cannot_add_duplicate_feed(self):
        subs_init = len(Subscription.objects.subs_for_user(self.user))
        self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/pagina12rss.xml"}
        )
        subs_before = len(Subscription.objects.subs_for_user(self.user))

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/pagina12rss.xml"}
        )
        my_subs = Subscription.objects.subs_for_user(self.user)
        subs_after = len(Subscription.objects.subs_for_user(self.user))

        self.assertEqual("El país | Página12", my_subs[subs_init].name)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subs_before, subs_after)

