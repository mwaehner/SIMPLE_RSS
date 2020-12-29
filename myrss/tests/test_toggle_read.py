
from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase

from myrss.models.article import Article
from myrss.models.article import SubscriptionArticle
from myrss.models.subscription import Subscription


def subscription_article_read_status(user_id, article_id):
    subscription_article = SubscriptionArticle.objects.filter(subscription__owner=user_id, article=article_id)
    return subscription_article.get().read




class ToggleReadTests(TestCase):
    def setUp(self):
        test_user = User.objects.get_or_create(username='testuser')
        self.client.force_login(test_user[0])
        self.user = User.objects.get(username='testuser')

    def test_user_article_is_toggled(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        article_id_to_toggle_read = 1

        self.assertFalse(subscription_article_read_status(self.user, article_id_to_toggle_read))
        response = self.client.post(
            "/toggle_read/" + str(article_id_to_toggle_read)+"/", follow=True, data={}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(subscription_article_read_status(self.user, article_id_to_toggle_read))


    def test_user_article_can_be_toggled_twice(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        article_id_to_toggle_read = 1

        self.assertFalse(subscription_article_read_status(self.user, article_id_to_toggle_read))
        response = self.client.post(
            "/toggle_read/" +str(article_id_to_toggle_read ) +"/", follow=True, data={}
        )
        response = self.client.post(
            "/toggle_read/" + str(article_id_to_toggle_read) + "/", follow=True, data={}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(subscription_article_read_status(self.user, article_id_to_toggle_read))

    def test_toggling_article_does_not_toggle_others(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        article_id_to_toggle_read = 1
        article_id_to_not_toggle_read = 2

        self.assertFalse(subscription_article_read_status(self.user, article_id_to_toggle_read))
        response = self.client.post(
            "/toggle_read/" +str(article_id_to_toggle_read ) +"/", follow=True, data={}
        )

        self.assertFalse(subscription_article_read_status(self.user, article_id_to_not_toggle_read))

    def test_cannot_toggle_not_existent_article(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        article_id_to_toggle_read = 123213214214124

        response = self.client.post(
            "/toggle_read/" + str(article_id_to_toggle_read) + "/", follow=True, data={}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)