from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase

from myrss.models.article import Article
from myrss.models.subscription import Subscription

def get_subscription_count_for(user):
    return len(Subscription.objects.subscriptions_for_user(user))

class UpdateSubscriptionViewTests(TestCase):
    def setUp(self):
        test_user = User.objects.get_or_create(username='testuser')
        self.client.force_login(test_user[0])
        self.user = User.objects.get(username='testuser')

    def test_updating_unchanged_subscription_brings_no_changes(self):
        response = self.client.post(
            "/new_subscription", data={"link": "test_utils/clarinrss.xml"}
        )
        subscription = Subscription.objects.get(owner=self.user)
        subscription_id = subscription.id
        article_count_before = len(subscription.article_set.all())

        response = self.client.post(
            "/update_subscription/" + str(subscription_id) + '/', data={}
        )
        article_count_after = len(Subscription.objects.get(owner=self.user).article_set.all())
        self.assertEqual(article_count_after, article_count_before)

    def test_updating_changed_subscription_brings_changes(self):
        response = self.client.post(
                "/new_subscription", data={"link": "test_utils/clarinrss.xml"}
        )
        subscription = Subscription.objects.get(owner=self.user)
        subscription_id = subscription.id
        article_count_before = len(subscription.article_set.all())
        subscription.link = "test_utils/clarinrss-updated.xml"
        subscription.save()
        added_number = 10
        #some article's titles (first, third, fourth and last)
        new_articles_titles = ["David Lamelas batalla por una obra nómade",
                               "Jubilados: los 4 puntos más conflictivos de la nueva ley de movilidad",
                               '''Para las Iglesias Evangélicas, "la Argentina retrocedió siglos" con la legalización del aborto''',
                               '''Quiniela de la Ciudad: resultado del sorteo de la Matutina de hoy, miércoles 30 de diciembre'''
                               ]

        response = self.client.post(
            "/update_subscription/" + str(subscription_id) + '/', data={}
        )
        article_count_after = len(Subscription.objects.get(owner=self.user).article_set.all())
        self.assertEqual(article_count_after, article_count_before +added_number)
        for article_title in new_articles_titles:
            self.assertTrue(Article.objects.filter(title=article_title).exists())


    def test_updating_changed_subscription_brings_no_changes_for_other_users(self):
        response = self.client.post(
                "/new_subscription", data={"link": "test_utils/clarinrss.xml"}
        )
        old_user = User.objects.get(username='testuser')
        another_test_user = User.objects.get_or_create(username='testuser2')
        self.client.force_login(another_test_user[0])
        self.user = User.objects.get(username='testuser2')
        response = self.client.post(
            "/new_subscription", data={"link": "test_utils/clarinrss.xml"}
        )
        subscription = Subscription.objects.get(owner=old_user)
        subscription_id = subscription.id
        article_count_before = len(subscription.article_set.all())

        subscription2 = Subscription.objects.get(owner=self.user)
        subscription2_id = subscription2.id
        subscription2.link = "test_utils/clarinrss-updated.xml"
        subscription2.save()


        response = self.client.post(
            "/update_subscription/" + str(subscription2_id) + '/', data={}
        )
        article_count_after = len(Subscription.objects.get(owner=old_user).article_set.all())
        self.assertEqual(article_count_after, article_count_before )