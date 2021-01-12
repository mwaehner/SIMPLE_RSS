from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase

from myrss.models.article import Article
from myrss.models.subscription import Subscription
from myrss.models.folder import Folder


class CreateFolderViewTests(TestCase):
    def setUp(self):
        test_user = User.objects.get_or_create(username='testuser')
        self.client.force_login(test_user[0])
        self.user = User.objects.get(username='testuser')

    def test_new_folder_is_correctly_added(self):
        response = self.client.post(
                "/new_folder", data={"name": "politica"}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Folder.objects.get().name, "politica")

    def test_multiple_folders_are_correctly_added(self):
        response = self.client.post(
                "/new_folder", data={"name": "politica"}
        )
        response = self.client.post(
            "/new_folder", data={"name": "eventos"}
        )
        response = self.client.post(
            "/new_folder", data={"name": "fulbo"}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Folder.objects.filter(name="politica").exists())
        self.assertTrue(Folder.objects.filter(name="eventos").exists())
        self.assertTrue(Folder.objects.filter(name="fulbo").exists())

    def test_duplicate_folder_cannot_be_added(self):
        response = self.client.post(
                "/new_folder", data={"name": "politica"}
        )
        response = self.client.post(
            "/new_folder", data={"name": "politica"}
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(len(Folder.objects.all()), 1)

    def test_two_users_can_have_a_folder_with_same_name(self):
        response = self.client.post(
                "/new_folder", data={"name": "politica"}
        )
        another_test_user = User.objects.get_or_create(username='testuser2')
        self.client.force_login(another_test_user[0])
        self.user = User.objects.get(username='testuser2')
        response = self.client.post(
            "/new_folder", data={"name": "politica"}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(Folder.objects.all()), 2)