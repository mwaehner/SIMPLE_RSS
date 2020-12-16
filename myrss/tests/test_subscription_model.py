from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase

from myrss.models.subscription_form import SubscriptionForm
from myrss.models.subscription_model import Subscription


class AddSubscriptionFormTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        self.user = User.objects.get(username='testuser')

    def test_form_from_invalid_link_is_invalid(self):
        subs = Subscription(from_user=self.user)
        sf = SubscriptionForm(instance=subs, data={"link": "asdas"})
        self.assertFalse(sf.is_valid())

    def test_form_from_invalid_rss_feed_is_invalid(self):
        subs = Subscription(from_user=self.user)
        sf = SubscriptionForm(instance=subs, data={"link": "https://www.google.com"})
        self.assertFalse(sf.is_valid())

    def test_form_from_valid_rss_feed_is_valid(self):
        subs = Subscription(from_user=self.user)
        sf = SubscriptionForm(instance=subs, data={"link": "https://www.clarin.com/rss/politica/"})
        self.assertTrue(sf.is_valid())

    def test_form_from_other_valid_rss_feed_is_valid(self):
        subs = Subscription(from_user=self.user)
        sf = SubscriptionForm(instance=subs, data={"link": "https://www.pagina12.com.ar/rss/secciones/el-pais/notas"})
        self.assertTrue(sf.is_valid())
