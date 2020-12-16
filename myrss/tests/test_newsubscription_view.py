from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase

from myrss.models.subscription_model import Subscription


class AddSubscriptionViewTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        self.user = User.objects.get(username='testuser')

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
            "/new_subscription", follow=True, data={"link": "https://www.google.com/"}
        )
        my_subs = Subscription.objects.subs_for_user(self.user)
        afteradding_subsno = len(my_subs)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subsno, afteradding_subsno)


    def test_valid_rss_feed_is_correctly_added(self):
        my_subs = Subscription.objects.subs_for_user(self.user)
        subsno = len(my_subs)

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "https://www.clarin.com/rss/politica/"}
        )
        my_subs = Subscription.objects.subs_for_user(self.user)
        afteradding_subsno = len(my_subs)

        self.assertEqual("Clarin.com - Política", my_subs[subsno].name)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subsno+1, afteradding_subsno)

    def test_another_valid_rss_feed_is_correctly_added(self):
        my_subs = Subscription.objects.subs_for_user(self.user)
        subsno = len(my_subs)

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "https://www.pagina12.com.ar/rss/secciones/el-pais/notas"}
        )
        my_subs = Subscription.objects.subs_for_user(self.user)
        afteradding_subsno = len(my_subs)

        self.assertEqual("El país | Página12", my_subs[subsno].name)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subsno+1, afteradding_subsno)


