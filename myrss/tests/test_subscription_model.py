from django.core.exceptions import ValidationError
from django.test import TestCase

from myrss.models.subscription_form import SubscriptionForm


class invalidRssRaisesError(TestCase):
    def test_raises_error(self):
        self.assertRaises(
            ValidationError, SubscriptionForm(data={"link": "https://www.google.com"})
        )
