from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .subscription_model import Subscription
import feedparser


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        exclude = ('from_user', 'name')

    def clean(self):
        link = self.cleaned_data.get("link")
        NewsFeed = feedparser.parse(link)
        if len(link) == 0 or NewsFeed.bozo: # NewsFeed.bozo se setea cuando el parsing falla
            raise ValidationError("Not a valid rss feed")
        title = feedparser.parse(link)['feed']['title']
        self.cleaned_data['name'] = title
        self.instance.name = title
        return self.cleaned_data

