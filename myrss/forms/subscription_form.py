from django.core.exceptions import ValidationError
from django.forms import ModelForm
from myrss.models.subscription import Subscription
from django.contrib.auth.models import User
import feedparser


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        exclude = ('owner', 'name')

    def clean(self):
        url = self.cleaned_data.get("link")
        if type(url)!=str or url == "":
            raise ValidationError("Please submit a nonempty link")
        news_feed = feedparser.parse(url)
        if news_feed.bozo: # news_feed.bozo se setea cuando el parsing falla
            raise ValidationError("Not a valid rss feed")
        with_this_link = Subscription.objects.filter(owner = self.instance.owner, link = url)
        if with_this_link.exists():
            raise ValidationError("You are already subscribed to this feed")
        try:
            title = feedparser.parse(url)['feed']['title']
            self.instance.name = title
        except Exception:
            raise ValidationError("Not a valid rss feed")
        return self.cleaned_data
