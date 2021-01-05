from django.contrib import admin
from .models.subscription import Subscription
from .models.article import Article
from .models.subscription_article import SubscriptionArticle
from django.db import models

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'link', 'name')
    list_filter = ('name', )
    search_fields = ['name']


@admin.register(SubscriptionArticle)
class SubscriptionArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'subscription', 'read')
    list_filter = ('subscription__name', 'read')
    search_fields = ['article__title']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'link', 'subscriptions_count')
    list_filter = ('subscriptions__name',)
    search_fields = ['title']

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('subscriptions'))
        return qs

    # useful for checking that we have no 0-subscription articles floating around the database
    def subscriptions_count(self, obj):
        return obj.subscriptions__count

    subscriptions_count.admin_order_field = 'subscriptions__count'
