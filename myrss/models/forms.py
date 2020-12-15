from django.forms import ModelForm

from .models import Subscription


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        exclude = ('from_user',)
