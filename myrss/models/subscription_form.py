from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .subscription_model import Subscription
import feedparser


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        exclude = ('from_user',)

    def clean(self):
        link = self.cleaned_data.get("link")
        NewsFeed = feedparser.parse(link)
        if NewsFeed.bozo: # este bit se setea cuando el parsing falla
            raise ValidationError("Not a valid rss feed")
        return self.cleaned_data

