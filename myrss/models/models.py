from django.db import models

from django.contrib.auth.models import User
from django.db.models import Q

class SubsQuerySet(models.QuerySet):
    def subs_for_user(self, user):
        return self.filter(
            from_user=user
        )


class Subscription(models.Model):
    from_user = models.ForeignKey(User, related_name="subscriber", on_delete=models.CASCADE)
    link = models.CharField(max_length=300)
    objects = SubsQuerySet.as_manager()

