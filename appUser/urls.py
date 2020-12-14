from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from .views import home, SignUpView

urlpatterns = [
    url(r'home$', home, name="user_home"),
    url(r'login$',
        LoginView.as_view(template_name="appUser/login_form.html"),
        name="user_login"),
    url(r'logout$',
        LogoutView.as_view(),
        name="user_logout"),
    url(r'signup$', SignUpView.as_view(), name='user_signup'),
]