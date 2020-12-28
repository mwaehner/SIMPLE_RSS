"""myrss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from myrss import settings

from myrss.views.home_view import HomeView
from myrss.views.welcome_view import WelcomeView
from myrss.views.signup_view import SignUpView
from myrss.views.home_view import HomeView
from myrss.views.new_subscription_view import NewSubscriptionView
from myrss.views.show_articles_view import ShowArticlesView
from myrss.views.update_subscription_view import UpdateSubscriptionView
from myrss.views.delete_subscription_view import DeleteSubscriptionView
from myrss.views.change_read_status_view import ChangeReadStatusView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', WelcomeView.as_view(), name="myrss_welcome"),
    url(r'^home$', HomeView.as_view(), name="user_home"),
    url(r'^login$',
        LoginView.as_view(template_name="myrss/login_form.html"),
        name="user_login"),
    url(r'^logout$',
        LogoutView.as_view(),
        name="user_logout"),
    url(r'^signup$', SignUpView.as_view(), name='user_signup'),
    url(r'new_subscription$', NewSubscriptionView.as_view(), name="new_subscription"),
    url(r'show_articles/(?P<subscription_id>\d+)/$', ShowArticlesView.as_view(), name="show_articles"),
    url(r'update_subscription/(?P<subscription_id>\d+)/$', UpdateSubscriptionView.as_view(), name="update_subscription"),
    url(r'delete_subscription/(?P<subscription_id>\d+)/$', DeleteSubscriptionView.as_view(), name="delete_subscription"),
    url(r'change_read_status/(?P<subscription_id>\d+)/(?P<article_id>\d+)/$', ChangeReadStatusView.as_view(), name="change_read_status"),
]
