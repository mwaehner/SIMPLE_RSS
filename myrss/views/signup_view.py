from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "appUser/signup_form.html"
    success_url = reverse_lazy('user_home')