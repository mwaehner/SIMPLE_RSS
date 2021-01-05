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


    def test_cannot_find_subscription_after_deleting_it(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        subscription_id = Subscription.objects.get(owner=self.user).id

        response = self.client.post(
            "/delete_subscription/" + str(subscription_id) + '/', follow=True, data={}
        )
        self.assertFalse(Subscription.objects.filter(pk=subscription_id))

    def test_deleting_subscription_does_not_alter_other_subscriptions(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/pagina12rss.xml"}
        )
        subscription_id = Subscription.objects.get(owner=self.user, link="test_utils/pagina12rss.xml").id

        response = self.client.post(
            "/delete_subscription/" + str(subscription_id) + '/', follow=True, data={}
        )
        self.assertFalse(Subscription.objects.filter(link="test_utils/pagina12rss.xml"))
        self.assertTrue(Subscription.objects.filter(link="test_utils/clarinrss.xml"))

    def test_deleting_subscription_from_user_does_not_delete_other_users_subscriptions(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        old_user = User.objects.get(username='testuser')
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
        subscriptions_no_after = get_subscription_count_for(old_user)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(subscriptions_no_before, subscriptions_no_after)
        self.assertEqual(Subscription.objects.get(owner=old_user).link, "test_utils/clarinrss.xml")

    def test_deleting_subscription_removes_articles_if_not_in_another_subscription(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )

        subscription_id = Subscription.objects.get(owner=self.user, link="test_utils/clarinrss.xml").id

        response = self.client.post(
            "/delete_subscription/" + str(subscription_id) + '/', follow=True, data={}
        )

        self.assertFalse(Article.objects.all())

    def test_deleting_subscription_does_not_remove_articles_if_in_another_subscription(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )

        another_test_user = User.objects.get_or_create(username='testuser2')
        self.client.force_login(another_test_user[0])
        self.user = User.objects.get(username='testuser2')
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        articles_count_before = len(Article.objects.all())

        subscription_id = Subscription.objects.get(owner=self.user, link="test_utils/clarinrss.xml").id

        response = self.client.post(
            "/delete_subscription/" + str(subscription_id) + '/', follow=True, data={}
        )
        articles_count_after = len(Article.objects.all())

        self.assertEqual(articles_count_after, articles_count_before)
