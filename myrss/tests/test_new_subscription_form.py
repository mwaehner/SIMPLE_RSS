from django.contrib.auth.models import User
from django.test import TestCase

from myrss.forms.subscription_form import SubscriptionForm
from myrss.models.subscription import Subscription


class NewSubscriptionFormTests(TestCase):
    def setUp(self):
        testUser = User.objects.get_or_create(username='testuser')
        self.client.force_login(testUser[0])
        self.user = User.objects.get(username='testuser')

    def test_form_from_valid_rss_feed_is_valid(self):
        subscription = Subscription(owner=self.user)
        subscription_form = SubscriptionForm(instance=subscription, data={"link": "test_utils/clarinrss.xml"}) #https://www.clarin.com/rss/politica/
        self.assertTrue(subscription_form.is_valid())

    def test_form_from_invalid_link_is_invalid(self):
        subscription = Subscription(owner=self.user)
        subscription_form = SubscriptionForm(instance=subscription, data={"link": "asdas"})
        self.assertFalse(subscription_form.is_valid())

    def test_form_from_invalid_rss_feed_is_invalid(self):
        subscription = Subscription(owner=self.user)
        subscription_form = SubscriptionForm(instance=subscription, data={"link": "test_utils/Google.html"})  #https://www.google.com
        self.assertFalse(subscription_form.is_valid())

    def test_form_from_other_valid_rss_feed_is_valid(self):
        subscription = Subscription(owner=self.user)
        subscription_form = SubscriptionForm(instance=subscription, data={"link": "test_utils/pagina12rss.xml"}) #https://www.pagina12.com.ar/rss/secciones/el-pais/notas
        self.assertTrue(subscription_form.is_valid())