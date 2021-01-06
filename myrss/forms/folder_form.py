from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms

from myrss.models.folder import Folder
from myrss.models.subscription import Subscription
from django.contrib.auth.models import User
import feedparser


class FolderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FolderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""
    class Meta:
        model = Folder
        exclude = ('subscriptions', 'owner')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Folder name'}),
        }

    def clean(self):
        name = self.cleaned_data.get("name")
        with_this_name = Folder.objects.filter(owner=self.instance.owner, name=name)
        if with_this_name.exists():
            raise ValidationError("You already have a folder with that name")
        return self.cleaned_data