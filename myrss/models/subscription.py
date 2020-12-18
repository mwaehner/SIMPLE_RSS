from django.contrib.auth.models import User
from django.db import models



class SubscriptionsQuerySet(models.QuerySet):
    def subscriptions_for_user(self, user):
        return self.filter(
            owner=user
        )


class Subscription(models.Model):
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    link = models.CharField(max_length=300)
    name = models.CharField(max_length=350)
    objects = SubscriptionsQuerySet.as_manager()


    class Meta:
        unique_together = ('link', 'owner',)

