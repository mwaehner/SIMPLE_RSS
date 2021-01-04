from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase

from myrss.models.article import Article
from myrss.models.article import SubscriptionArticle
from myrss.models.subscription import Subscription


def article_is_read(user_id, article_id):
    subscription_article = SubscriptionArticle.objects.filter(subscription__owner=user_id, article=article_id)
    return subscription_article.get().read




class SetReadTests(TestCase):
    def setUp(self):
        test_user = User.objects.get_or_create(username='testuser')
        self.client.force_login(test_user[0])
        self.user = User.objects.get(username='testuser')

    def test_setting_article_as_read_marks_it_as_read(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        article_id = 1

        response = self.client.post(
            "/set_read/" + str(article_id) + "/", follow=True, data={}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(article_is_read(self.user, article_id))

    def test_setting_article_as_read_twice_marks_it_as_read(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        article_id = 1

        response = self.client.post(
            "/set_read/" + str(article_id) + "/", follow=True, data={}
        )
        response = self.client.post(
            "/set_read/" + str(article_id) + "/", follow=True, data={}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(article_is_read(self.user, article_id))

    def test_setting_article_does_not_set_others(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        article_id_to_set_read = 1
        article_id_to_not_set_read = 2

        self.assertFalse(article_is_read(self.user, article_id_to_not_set_read))
        response = self.client.post(
            "/set_read/" +str(article_id_to_set_read) + "/", follow=True, data={}
        )

        self.assertFalse(article_is_read(self.user, article_id_to_not_set_read))

    def test_setting_article_does_not_impact_other_users_articles(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        old_user = User.objects.get(username='testuser')
        another_test_user = User.objects.get_or_create(username='testuser2')
        self.client.force_login(another_test_user[0])
        self.user = User.objects.get(username='testuser2')

        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        article_id_to_toggle_read = 1

        response = self.client.post(
            "/set_read/" + str(article_id_to_toggle_read) + "/", follow=True, data={}
        )
        self.assertTrue(article_is_read(self.user, article_id_to_toggle_read))
        self.assertFalse(article_is_read(old_user, article_id_to_toggle_read))