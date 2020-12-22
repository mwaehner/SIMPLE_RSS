from django.contrib.auth.models import User
from django.db import models

class SubscriptionQuerySet(models.QuerySet):
    def subscriptions_for_user(self, user):
        return self.filter(
            owner=user
        )


class Subscription(models.Model):
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    link = models.CharField(max_length=300)
    name = models.CharField(max_length=350)
    objects = SubscriptionQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('link', 'owner',)

