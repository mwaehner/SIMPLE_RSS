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

from myrss.views.views import Home, SignUpView, Welcome

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Welcome.as_view(), name="myrss_welcome"),
    url(r'^home$', Home.as_view(), name="user_home"),
    url(r'^login$',
        LoginView.as_view(template_name="appUser/login_form.html"),
        name="user_login"),
    url(r'^logout$',
        LogoutView.as_view(),
        name="user_logout"),
    url(r'^signup$', SignUpView.as_view(), name='user_signup'),
]

