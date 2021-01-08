from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase

from myrss.models.article import Article
from myrss.models.subscription import Subscription
from myrss.models.folder import Folder


class NewFolderViewTests(TestCase):
    def setUp(self):
        test_user = User.objects.get_or_create(username='testuser')
        self.client.force_login(test_user[0])
        self.user = User.objects.get(username='testuser')

    def test_cannot_add_subscription_to_non_existent_folder(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        subscription = Subscription.objects.get()
        response = self.client.post(
                "/add_subscriptions_to_folder", data={"folder": "politica",
                                                       'subscriptions': str([subscription.id])
                                                       }
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertFalse(subscription.folder_set.all())

    def test_existent_subscription_is_correctly_added_to_existent_folder(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        response = self.client.post(
            "/new_folder", data={"name": "politica"}
        )
        subscription = Subscription.objects.get()
        response = self.client.post(
            "/add_subscriptions_to_folder", data={"folder": "politica",
                                                  'subscriptions': str([subscription.id])
                                                  }
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(subscription.folder_set.get().name, "politica")

    def test_existent_subscription_is_correctly_added_to_multiple_folders(self):
        response = self.client.post(
            "/new_subscription", follow=True, data={"link": "test_utils/clarinrss.xml"}
        )
        response = self.client.post(
            "/new_folder", data={"name": "politica"}
        )
        response = self.client.post(
            "/new_folder", data={"name": "eventos"}
        )

        subscription = Subscription.objects.get()
        response = self.client.post(
            "/add_subscriptions_to_folder", data={"folder": "politica",
                                                  'subscriptions': str([subscription.id])
                                                  }
        )
        response = self.client.post(
            "/add_subscriptions_to_folder", data={"folder": "eventos",
                                                  'subscriptions': str([subscription.id])
                                                  }
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(subscription.folder_set.filter(name="politica").exists())
        self.assertTrue(subscription.folder_set.filter(name="eventos").exists())