from django.contrib import admin
from .models.subscription import Subscription
from .models.article import Article
from django.db import models

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'link', 'name')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'title', 'subscriptions_count')

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('subscriptions'))
        return qs

    # useful for checking that we have no 0-subscription articles floating around the database
    def subscriptions_count(self, obj):
        return obj.subscriptions__count

    subscriptions_count.admin_order_field = 'subscriptions__count'
