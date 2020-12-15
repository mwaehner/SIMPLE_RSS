from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator



class HomeView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'appUser/home.html')