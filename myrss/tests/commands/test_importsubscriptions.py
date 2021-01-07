from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth.models import User

from myrss.models.article import Article
from myrss.models.subscription import Subscription

class ImportSubscriptionsTest(TestCase):
    def setUp(self):
        testUser = User.objects.get_or_create(username='testuser')
        self.user = User.objects.get(username='testuser')

    def test_command_creates_subscriptions_if_rss_is_valid(self):
        out = StringIO()
        subscriptions_opml_file = ['test_utils/opml_subscriptions.xml']
        user_ids = [self.user.id]
        call_command("importsubscriptions", subscriptions=subscriptions_opml_file, user_ids=user_ids, stdout=out)
        self.assertTrue(Subscription.objects.filter(owner=self.user, name="Clarin - Lo último").exists())
        self.assertTrue(Subscription.objects.filter(owner=self.user, name="Página 12").exists())

    def test_command_does_not_create_subscriptions_if_rss_is_invalid(self):
        out = StringIO()
        subscriptions_opml_file = ['test_utils/opml_subscriptions_invalid.xml']
        user_ids = [self.user.id]
        call_command("importsubscriptions", subscriptions=subscriptions_opml_file, user_ids=user_ids, stdout=out)
        self.assertFalse(Subscription.objects.all())

    def test_command_creates_subscriptions_for_multiple_users(self):
        out = StringIO()
        subscriptions_opml_file = ['test_utils/opml_subscriptions.xml']
        another_test_user = User.objects.create(username='testuser2')
        user_ids = [self.user.id, another_test_user.id]
        call_command("importsubscriptions", subscriptions=subscriptions_opml_file, user_ids=user_ids, stdout=out)
        self.assertTrue(Subscription.objects.filter(owner=self.user, name="Clarin - Lo último").exists())
        self.assertTrue(Subscription.objects.filter(owner=another_test_user, name="Clarin - Lo último").exists())


    def test_command_creates_subscriptions_for_all_users_if_none_was_specified(self):
        out = StringIO()
        subscriptions_opml_file = ['test_utils/opml_subscriptions.xml']
        another_test_user = User.objects.create(username='testuser2')
        yet_another_test_user = User.objects.create(username='testuser3')
        user_ids = []
        call_command("importsubscriptions", subscriptions=subscriptions_opml_file, user_ids=user_ids, stdout=out)
        self.assertTrue(Subscription.objects.filter(owner=self.user, name="Clarin - Lo último").exists())
        self.assertTrue(Subscription.objects.filter(owner=another_test_user, name="Clarin - Lo último").exists())
        self.assertTrue(Subscription.objects.filter(owner=yet_another_test_user, name="Clarin - Lo último").exists())

    def test_command_fetchs_articles_if_rss_is_valid(self):
        out = StringIO()
        subscriptions_opml_file = ['test_utils/opml_subscriptions.xml']
        user_ids = [self.user.id]
        call_command("importsubscriptions", subscriptions=subscriptions_opml_file, user_ids=user_ids, stdout=out)
        subscription_id = Subscription.objects.get(owner=self.user, name="Clarin - Lo último").id
        self.assertTrue(Article.objects.filter(subscriptions__id=subscription_id,
            link="https://www.clarin.com/mundo/brasil-presenta-plan-vacunacion-coronavirus-bolsonaro-dice-vacunara-virus-lluvia-va-afectar-_0_34r4DbcUe.html").exists())
        self.assertTrue(Article.objects.filter(subscriptions__id=subscription_id,
            link="https://www.clarin.com/internacional/estados-unidos/hijos-padres-familia-poliamorosa-hombres-reconocida-legalmente_0_I6qO_KBCN.html").exists())