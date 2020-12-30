from django.contrib import admin
from .models.subscription import Subscription
from .models.article import Article, SubscriptionArticle
from django.db import models

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'link', 'name')


@admin.register(SubscriptionArticle)
class SubscriptionArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'subscription', 'read')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'title', 'subscriptions_no')

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('subscriptions'))
        return qs

    # useful for checking that we have no 0-subscription articles floating around the database
    def subscriptions_no(self, obj):
        return obj.subscriptions__count

    subscriptions_no.admin_order_field = 'subscriptions__count'
