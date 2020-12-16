from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .subscription_model import Subscription
from django.contrib.auth.models import User
import feedparser


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        exclude = ('from_user', 'name')

    def clean(self):
        url = self.cleaned_data.get("link")
        NewsFeed = feedparser.parse(url)
        if NewsFeed.bozo: # NewsFeed.bozo se setea cuando el parsing falla
            raise ValidationError("Not a valid rss feed")
        noWithThisLink = Subscription.objects.filter(from_user = self.instance.from_user, link = url).count()
        if noWithThisLink != 0:
            raise ValidationError("You are already subscribed to this feed")
        try:
            title = feedparser.parse(url)['feed']['title']
            self.cleaned_data['name'] = title
            self.instance.name = title
        except Exception:
            raise ValidationError("Not a valid rss feed")
        return self.cleaned_data
